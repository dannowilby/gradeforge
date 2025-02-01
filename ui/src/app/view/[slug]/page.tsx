"use client"

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation"

export default function Report() {
    const pathname = usePathname()
    const student_id = pathname.split("/").at(-1);

    const [data, setData] = useState<string[][] | null>(null);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
      fetch(`http://localhost:3000/view/${student_id}`).then(res => res.json())
        .then(data => {
          setData(data)
          setLoading(false)
        })
    }, [student_id])

    if (isLoading || data == null)
      return (
        <div className="w-1/3 mx-auto my-12 skeleton h-[25vh]" />
      )

    return (
      <div className="w-1/3 mx-auto my-12">
        <h1 className="font-bold">{data.length > 0 && data[0][0]}</h1>
        <h2>{student_id}</h2>

        <table className="table my-8">
          <thead>
            <tr>
              <th>Date</th>
              <th>Response</th>
            </tr>
          </thead>
          <tbody>
            {data.map(([, report, date], index) => (
              <tr key={index}>
                <td>{date}</td>
                <td>{report}</td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>
    );
}