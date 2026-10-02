// STRING with literal // still a string; slashes inside strings are preserved.
"// still a string"

// PRINT STRING SEMICOLON; trailing comment produces no tokens.
print "done"; // ignored: @ ! == 123 "not a token"

// STRING with an empty
""

// STRING with number
"123"

// STRING nothing is treated as a comment
"// This is a test"

// STRING no unexpected is treated as a comment
"$#&"
