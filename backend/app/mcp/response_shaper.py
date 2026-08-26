from typing import Any


class ResponseShaper:

    @staticmethod
    def shape(
        data: Any,
        fields: list[str] | None,
    ) -> Any:

        if not fields:
            return data

        return ResponseShaper._process(
            value=data,
            fields=fields,
        )

    @staticmethod
    def _process(
        value: Any,
        fields: list[str],
    ) -> Any:

        if isinstance(value, list):

            return [
                ResponseShaper._process(
                    item,
                    fields,
                )
                for item in value
            ]

        if isinstance(value, dict):

            # If this dictionary directly contains
            # requested fields, shape it.
            matching_fields = {
                field: value[field]
                for field in fields
                if field in value
            }

            if matching_fields:

                return matching_fields

            # Otherwise continue recursively.
            return {
                key: ResponseShaper._process(
                    value=item,
                    fields=fields,
                )
                for key, item in value.items()
                if isinstance(item, (dict, list))
            }

        return value