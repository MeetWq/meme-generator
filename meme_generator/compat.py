"""本模块为 Pydantic 版本兼容层模块

为兼容 Pydantic V1 与 V2 版本，定义了一系列兼容函数与类供使用。
"""

from typing import Any, Optional, TypeVar, Union

from pydantic import VERSION, BaseModel

T = TypeVar("T")

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2


__all__ = (
    "model_dump",
    "model_json_schema",
    "type_validate_python",
    "type_validate_json",
)


if PYDANTIC_V2:  # pragma: pydantic-v2
    from pydantic import TypeAdapter as TypeAdapter
    from pydantic.json_schema import DEFAULT_REF_TEMPLATE

    def model_dump(
        model: BaseModel,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        return model.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def model_json_schema(
        model: type[BaseModel],
        by_alias: bool = True,
        ref_template: str = DEFAULT_REF_TEMPLATE,
    ) -> dict[str, Any]:
        return model.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    def type_validate_python(type_: type[T], data: Any) -> T:
        """Validate data with given type."""
        return TypeAdapter(type_).validate_python(data)

    def type_validate_json(type_: type[T], data: Union[str, bytes]) -> T:
        """Validate JSON with given type."""
        return TypeAdapter(type_).validate_json(data)


else:  # pragma: pydantic-v1
    from pydantic import parse_obj_as, parse_raw_as
    from pydantic.schema import default_ref_template

    def model_dump(
        model: BaseModel,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        return model.dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def model_json_schema(
        model: type[BaseModel],
        by_alias: bool = True,
        ref_template: str = default_ref_template,
    ) -> dict[str, Any]:
        return model.schema(by_alias=by_alias, ref_template=ref_template)

    def type_validate_python(type_: type[T], data: Any) -> T:
        """Validate data with given type."""
        return parse_obj_as(type_, data)

    def type_validate_json(type_: type[T], data: Union[str, bytes]) -> T:
        """Validate JSON with given type."""
        return parse_raw_as(type_, data)
