
# GradeForge

This is a reimplementation of the first report card generator I made in late 2023. The extension contains code used to scrape the company's admin pages, and I have made that code private due to the potential risk of exposing sensitive details inadvertently.

As an internal tool the interface is not flashy, just doing what it needs to.

The following shows example data and the generated response from Claude for a non-existent student:
```
student_id: "103448"
student_name: "Last, First"
behavior_comments {
  date {
    seconds: 1484248326
  }
  comment: "Worked well, struggled with multi-digit subtraction but got it by the end of the sesion"
  pages_completed: 4
}
behavior_comments {
  date {
    seconds: 1484248326
  }
  comment: "Was pretty distracted by people around them"
  pages_completed: 3
}
total_plan_length: 12
updated_lessons {
  name: "[PK104] Multidigit subtraction"
  completed: true
}
updated_lessons {
  name: "[PK1055] Geometric shapes: Triangles and Squares"
}
updated_lessons {
  name: "[PK64] Advanced Number patterns"
}
updated_lessons {
  name: "[PK999] Reasoning by grouping"
}
```

The object serializes to the following byte string:

`'\n\x06103448\x12\x0bLast, First"c\n\x06\x08\x86\xaa\xdf\xc3\x05\x12WWorked well, struggled with multi-digit subtraction but got it by the end of the sesion\x18\x04"7\n\x06\x08\x86\xaa\xdf\xc3\x05\x12+Was pretty distracted by people around them\x18\x03(\x0c2"\n\x1e[PK104] Multidigit subtraction\x10\x0122\n0[PK1055] Geometric shapes: Triangles and Squares2!\n\x1f[PK64] Advanced Number patterns2\x1f\n\x1d[PK999] Reasoning by grouping'`

And to start the generation, send the data to the server:
`curl -X POST --data-raw $'\n\x06103348\x12\nNAme, Test(\x04' http://localhost:3000/generate`

This is the result:
```
First has shown good progress in their math work. They demonstrated particularly strong improvement with multi-digit subtraction, mastering the concept by the end of their session. Currently, they are working on geometric shapes, number patterns, and reasoning by grouping. First typically completes 3-4 pages per session.
```
