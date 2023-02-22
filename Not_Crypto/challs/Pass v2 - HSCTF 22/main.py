#!/usr/bin/env python3
import string

def main():
	allowed_chars = string.ascii_letters + string.digits + ",!+-/@&|~^<>(){}"
	allowed_globals = vars(__builtins__).copy()
	for var in (
		"getattr", "eval", "exec", "__import__", "open", "__builtins__", "__build_class__",
		"__loader__", "__spec__"
	):
		allowed_globals[var] = None
	
	print("Python as a Service:")
	print("Execute arbitrary Python code (with certain restrictions)")
	while True:
		try:
			s = input("> ")
		except (EOFError, KeyboardInterrupt):
			exit()
		if not s:
			continue
		if any(c not in allowed_chars for c in s):
			print("Illegal characters")
			continue
		try:
			print(eval(s, allowed_globals))
		except Exception as e:
			print(e)

if __name__ == "__main__":
	main()
