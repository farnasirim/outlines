import os

from outlines.text.models import LanguageModel

try:
    import openai
    from openai import error
except ImportError:
    raise ImportError("You need to install `openai` to run OpenAI's language models.")


class OpenAI(LanguageModel):
    """Represents any of OpenAI's language models

    You should have the `openai` package installed, and store you OpenAI key in
    the `OPENAI_API_KEY` environment variable.

    """

    def __init__(self, model: str):
        """Initialize the OpenAI model."""

        try:
            self.openai_api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            raise OSError(
                "Could not find the `OPENAI_API_KEY` environment variable. Please make sure it is set to your OpenAI key before re-running your model."
            )

        available_models = openai.Model.list()
        available_model_names = [model["id"] for model in available_models["data"]]
        if model not in available_model_names:
            raise OSError(f"{model} is not a valid OpenAI model name.")

        super().__init__(name=f"OpenAI {model}")
        self.model = model

    def perform(self, prompt):
        try:
            resp = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=128,
            )
        except error.APIConnectionError as e:
            raise OSError(f"Open API failed to connect: {e}")
        except error.AuthenticationError as e:
            raise OSError(
                f"Open API request not authorized: {e}. Check that the token provided is valid."
            )
        except error.PermissionError as e:
            raise OSError(f"Open API request was not permitted: {e}")
        except error.RateLimitError as e:
            raise OSError(
                f"Open API requests exceeded the rate limit: {e}. Wait before re-running your program."
            )
        except error.Timeout as e:
            raise OSError(f"Open API request timed out: {e}")

        return resp["choices"][0]["text"]
