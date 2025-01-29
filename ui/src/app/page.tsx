
export default function Home() {
  return (
    <div className="w-1/3 mx-auto my-12">
      <h1 className="text-2xl font-bold">GradeForge</h1>

      <p className="my-3">
        GradeForge is used to create and view report cards automatically. Download and install the extension to get started.
      </p>

      <p className="mb-3">Usage documentation can be found at this <a className="link" href="https://github.com/dannowilby/gradeforge">link</a>. Report any issues <a className="link" href="https://github.com/dannowilby/gradeforge/issues">here</a>.</p>

      <a className="link block" href="/view">View reports</a>
    </div>
  );
}
