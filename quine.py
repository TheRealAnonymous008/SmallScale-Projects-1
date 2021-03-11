def main():
 program = [
  "def main():",
  " program = [",
  "",
  " ]",
  " i = 1",
  " for p in program:",
  "  if i == 2:",
  "   for s in program:",
  "    u = s.replace(\"\\\\\", \"\\\\\\\\\")",
  "    v = u.replace(\"\\\"\", \"\\\\\\\"\")",
  "    print(str(\" \\\"\") + v + str(\"\\\",\"))",
  "  else:",
  "   print(p)",
  "  i+=1",
  "",
  "main()",
 ]
 i = 1
 for p in program:
  if i == 3:
   for s in program:
    u = s.replace("\\", "\\\\")
    v = u.replace("\"", "\\\"")
    print(str("  \"") + v + str("\","))
  else:
   print(p)
  i+=1 

main()
