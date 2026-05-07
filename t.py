

import inspect


def format_annotation(annotation):
    if annotation is inspect._empty:
        return "Any"

    if hasattr(annotation, "__name__"):
        return annotation.__name__

    return str(annotation).replace("typing.", "")


def dump_client_api(cls):
    seen = set()

    print(f"# {cls.__name__}\n")

    # идем по inheritance chain
    for base in cls.__mro__:

        # пропускаем мусор
        if base.__module__.startswith("builtins"):
            continue

        methods = []

        for name, func in inspect.getmembers(base):

            if name.startswith("_"):
                continue

            if name in seen:
                continue

            if not (
                inspect.isfunction(func)
                or inspect.ismethod(func)
                or inspect.iscoroutinefunction(func)
            ):
                continue

            seen.add(name)

            sig = inspect.signature(func)

            params = []

            for param in sig.parameters.values():

                if param.name in ("self", "cls"):
                    continue

                ann = format_annotation(param.annotation)

                default = ""

                if param.default is not inspect._empty:
                    default = f" = {param.default!r}"

                params.append(
                    f"{param.name}: {ann}{default}"
                )

            returns = format_annotation(
                sig.return_annotation
            )

            prefix = "async " if inspect.iscoroutinefunction(func) else ""

            methods.append(
                f"{prefix}{name}({', '.join(params)}) -> {returns}"
            )

        if methods:
            print(f"## {base.__name__}\n")

            for method in sorted(methods):
                print(method)

            print()


from kyodo.api import *

for x in[AuthModule, CommonModule, ChatModule, UserModule, CircleModule,
	CircleAdminModule, BlogModule]:
    dump_client_api(x)


print("\n\nASYNC:")

from kyodo.api._async import *
for x in[AuthModule, CommonModule, ChatModule, UserModule, CircleModule,
	CircleAdminModule, BlogModule]:
    dump_client_api(x)
