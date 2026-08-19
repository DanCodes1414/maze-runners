#!/usr/bin/env python3

lines = ["ello", "ha", "hi", "hy" "there", "my", "friend"]


print(f"before: {lines}")

for line in lines:
    if line[0] == 'h':
        lines.remove(line)

print(f"after: {lines}")

non_h_lines = []

print(f"before: {non_h_lines}")

for line in lines:
    if line[0] != 'h':
        non_h_lines.append(line)

print(f"after: {non_h_lines}")