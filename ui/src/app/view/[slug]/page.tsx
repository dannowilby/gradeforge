"use client"

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation"

export default function Report() {
    const pathname = usePathname()

    const [data, setData] = useState(null);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
      fetch(`http://localhost:3000/view/${pathname.split("/").at(-1)}`).then(res => res.json())
        .then(data => {
          console.log(data);
          setData(data)
          setLoading(false)
        })
    }, [])

    return <div className="w-1/3 mx-auto my-12"><p>{pathname}</p></div>
}