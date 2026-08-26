from typing import Any


class ResponseShaper:

    @staticmethod
    def shape(
        data: Any,
        fields: list[str],
    ) -> Any:

        if not fields:
            return data

        if isinstance(data, list):

            return [
                ResponseShaper.shape(
                    item,
                    fields,
                )
                for item in data
            ]

        if isinstance(data, dict):

            return {
                key: value
                for key, value in data.items()
                if key in fields
            }

        return data