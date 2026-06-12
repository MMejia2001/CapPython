from pathlib import Path
from grpc_tools import protoc


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    proto_dir = root / "proto"
    output_dir = root / "src" / "lab_interop" / "generated"
    proto_file = proto_dir / "orders.proto"

    return protoc.main(
        [
            "grpc_tools.protoc",
            f"-I{proto_dir}",
            f"--python_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            str(proto_file),
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
