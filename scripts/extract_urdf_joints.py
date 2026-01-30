#!/usr/bin/env python3
"""
Extract joint order and limit data from a URDF for RobotConfig lists.

Usage:
  python scripts/extract_urdf_joints.py path/to/robot.urdf
"""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET


def parse_urdf(path: str):
    root = ET.parse(path).getroot()

    # Preserve URDF order
    dof_names: list[str] = []
    lower: list[float] = []
    upper: list[float] = []
    velocity: list[float] = []
    effort: list[float] = []

    for joint in root.findall("joint"):
        jtype = joint.attrib.get("type")
        if jtype not in ("revolute", "prismatic", "continuous"):
            continue
        name = joint.attrib.get("name")
        if not name:
            continue
        dof_names.append(name)

        limit = joint.find("limit")
        if limit is None or jtype == "continuous":
            # Use None for missing limits; caller can decide how to fill.
            lower.append(None)
            upper.append(None)
            velocity.append(None)
            effort.append(None)
        else:
            lower.append(float(limit.attrib.get("lower", "0")))
            upper.append(float(limit.attrib.get("upper", "0")))
            velocity.append(float(limit.attrib.get("velocity", "0")))
            effort.append(float(limit.attrib.get("effort", "0")))

    links = [link.attrib.get("name") for link in root.findall("link") if link.attrib.get("name")]

    return {
        "dof_names": dof_names,
        "dof_pos_lower_limit_list": lower,
        "dof_pos_upper_limit_list": upper,
        "dof_vel_limit_list": velocity,
        "dof_effort_limit_list": effort,
        "link_names": links,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract URDF joint order and limits")
    parser.add_argument("urdf", help="Path to URDF file")
    parser.add_argument("--format", choices=["python", "json"], default="python")
    args = parser.parse_args()

    data = parse_urdf(args.urdf)

    if args.format == "json":
        print(json.dumps(data, indent=2))
        return

    # Python snippet output
    print(f"# DOF count: {len(data['dof_names'])}")
    print("dof_names = [")
    for name in data["dof_names"]:
        print(f"    {name!r},")
    print("]\n")

    def _print_list(name: str):
        print(f"{name} = [")
        for v in data[name]:
            print(f"    {v},")
        print("]\n")

    _print_list("dof_pos_lower_limit_list")
    _print_list("dof_pos_upper_limit_list")
    _print_list("dof_vel_limit_list")
    _print_list("dof_effort_limit_list")

    print(f"# Link count: {len(data['link_names'])}")
    print("link_names = [")
    for name in data["link_names"]:
        print(f"    {name!r},")
    print("]")


if __name__ == "__main__":
    main()
