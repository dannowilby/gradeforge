"use client"

import Link from "next/link";
import { useEffect, useState } from "react";

export default function View() {

    const [data, setData] = useState<string[][] | null>(null);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
      fetch(`http://localhost:${process.env.NEXT_PUBLIC_PORT}/view`).then(res => res.json())
        .then(data => {
          setData(data)
          setLoading(false)
        })
    }, [])

    if (isLoading) 
      return (
        <div className="w-1/3 mx-auto my-12 skeleton h-[25vh]" />
      )

    return (
      <div className="w-1/3 mx-auto my-12">
        <h1 className="text-xl font-bold">Students</h1>
        {data != null && data.map(([student_id, student_name], i) => (
          <Link className="link block my-2" key={i} href={`/view/${student_id}`}>{student_name}</Link>
        ))}
      </div>
    );
  }
  