import { useEffect, useRef, useState } from "react";

type Language = "en" | "es";
type RecognitionType = "page" | "text_formula" | "formula" | "text";

const recognitionOptions: Array<{ value: RecognitionType; label: string }> = [
  { value: "page", label: "Page" },
  { value: "text_formula", label: "Text and formulas" },
  { value: "formula", label: "Formula" },
  { value: "text", label: "Text" },
];

function App() {
  const [selectedFile, setSelectedFile] = useState<File>();
  const [language, setLanguage] = useState<Language>("en");
  const [recognitionType, setRecognitionType] =
    useState<RecognitionType>("text_formula");
  const [markdown, setMarkdown] = useState("");
  const [message, setMessage] = useState("");
  const [isConverting, setIsConverting] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  const setFile = (file: File | undefined) => {
    if (!file || !file.type.startsWith("image/")) {
      setMessage("Please select an image.");
      return;
    }
    setSelectedFile(file);
    setMessage("");
  };

  useEffect(() => {
    const handlePaste = (event: ClipboardEvent) => {
      const item = Array.from(event.clipboardData?.items ?? []).find((entry) =>
        entry.type.startsWith("image/"),
      );
      if (!item) return;
      event.preventDefault();
      setFile(item.getAsFile() ?? undefined);
    };
    document.addEventListener("paste", handlePaste);
    return () => document.removeEventListener("paste", handlePaste);
  }, []);

  const convert = async () => {
    if (!selectedFile) {
      setMessage("Paste or select an image first.");
      return;
    }

    const data = new FormData();
    data.append("image", selectedFile);
    data.append("language", language);
    data.append("recognition_type", recognitionType);
    setIsConverting(true);
    setMessage("Processing...");

    try {
      const response = await fetch("/api/convert", {
        method: "POST",
        body: data,
      });
      const body = (await response.json()) as { markdown?: string; detail?: string };
      if (!response.ok) throw new Error(body.detail || "Conversion failed.");
      setMarkdown(body.markdown ?? "");
      setMessage("");
    } catch (reason) {
      setMessage(reason instanceof Error ? reason.message : "Conversion failed.");
    } finally {
      setIsConverting(false);
    }
  };

  const copyMarkdown = async () => {
    await navigator.clipboard.writeText(markdown);
    setMessage("Markdown copied.");
  };

  const downloadMarkdown = () => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(
      new Blob([markdown], { type: "text/markdown" }),
    );
    link.download = "pix2text.md";
    link.click();
    URL.revokeObjectURL(link.href);
  };

  return (
    <main>
      <h1>Pix2Text</h1>
      <p>Paste an image or choose one to convert it to Markdown.</p>

      <div className="settings">
        <label>
          Language:
          <select value={language} onChange={(event) => setLanguage(event.target.value as Language)}>
            <option value="en">English</option>
            <option value="es">Spanish</option>
          </select>
        </label>
        <label>
          Recognition type:
          <select
            value={recognitionType}
            onChange={(event) => setRecognitionType(event.target.value as RecognitionType)}
          >
            {recognitionOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>
      </div>

      <button
        className="drop"
        type="button"
        onClick={() => fileInput.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          setFile(event.dataTransfer.files[0]);
        }}
      >
        Paste an image here, or <span>choose a file</span>
      </button>
      <input
        ref={fileInput}
        className="file-input"
        type="file"
        accept="image/*"
        onChange={(event) => setFile(event.target.files?.[0])}
      />
      <p className="filename">{selectedFile?.name ?? ""}</p>

      <div className="actions">
        <button type="button" onClick={convert} disabled={isConverting}>
          {isConverting ? "Converting..." : "Convert"}
        </button>
        <button type="button" onClick={copyMarkdown} disabled={!markdown}>Copy Markdown</button>
        <button type="button" onClick={downloadMarkdown} disabled={!markdown}>Download Markdown</button>
      </div>
      <p className="message" role="alert">{message}</p>
      <h2>Markdown</h2>
      <textarea value={markdown} readOnly spellCheck={false} />
    </main>
  );
}

export default App;
