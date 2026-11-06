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
  const [copied, setCopied] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [previewUrl, setPreviewUrl] = useState("");
  const fileInput = useRef<HTMLInputElement>(null);

  const setFile = (file: File | undefined) => {
    if (!file || !file.type.startsWith("image/")) {
      setMessage("Please select an image.");
      return;
    }
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    void convert(file);
  };

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

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

  const convert = async (file = selectedFile) => {
    if (!file) {
      setMessage("Paste or select an image first.");
      return;
    }

    const data = new FormData();
    data.append("image", file);
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
  };

  return (
    <main className="app-shell">
      <label className="field-label" htmlFor="language">Language</label>
        <select
          id="language"
          className="select"
          value={language}
          onChange={(event) => setLanguage(event.target.value as Language)}
        >
            <option value="en">English</option>
            <option value="es">Spanish</option>
        </select>

        <label className="field-label" htmlFor="recognition-type">Recognition type</label>
        <select
          id="recognition-type"
          className="select"
          value={recognitionType}
          onChange={(event) => setRecognitionType(event.target.value as RecognitionType)}
        >
          {recognitionOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>

      <button
        className={`drop-zone${isDragging ? " dragging" : ""}`}
        type="button"
        onClick={() => fileInput.current?.click()}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setIsDragging(false);
          setFile(event.dataTransfer.files[0]);
        }}
      >
        <svg className="upload-icon" aria-hidden="true" viewBox="0 0 24 24">
          <path d="M13 3v9.586l3.5-3.5 1.414 1.414L12 16.414 6.086 10.5 7.5 9.086l3.5 3.5V3H13ZM4.5 14v5h15v-5h2v7h-19v-7h2Z" />
        </svg>
        <strong>Drop or paste an image, or click to select</strong>
        <span className="drop-help">Supports drag and drop, Ctrl+V, and image files</span>
        {previewUrl && <img className="preview" src={previewUrl} alt="Selected image preview" />}
      </button>
      <input
        ref={fileInput}
        className="file-input"
        type="file"
        accept="image/*"
        onChange={(event) => setFile(event.target.files?.[0])}
      />
      <p className="filename">{selectedFile?.name ?? "No image selected"}</p>

      {message && <p className={`message${message === "Processing..." ? " processing" : ""}`} role="alert">{message}</p>}
      {selectedFile && (
        <section className="result-card">
          <div className="result-header">
            <span>Result</span>
            <button
              className={`copy-button${copied ? " copied" : ""}`}
              type="button"
              onClick={async () => {
                await copyMarkdown();
                setCopied(true);
                window.setTimeout(() => setCopied(false), 1200);
              }}
              disabled={!markdown}
              aria-label={copied ? "Markdown copied" : "Copy Markdown"}
              title={copied ? "Copied" : "Copy Markdown"}
            >
              {copied ? (
                <svg aria-hidden="true" viewBox="0 0 16 16">
                  <path d="m2.75 8.75 3.5 3.5 7-7.5" />
                </svg>
              ) : (
                <svg aria-hidden="true" viewBox="0 0 48 48">
                  <path d="M13 12.432v-4.62A2.813 2.813 0 0 1 15.813 5h24.374A2.813 2.813 0 0 1 43 7.813v24.375A2.813 2.813 0 0 1 40.187 35h-4.67" />
                  <path d="M32.188 13H7.811A2.813 2.813 0 0 0 5 15.813v24.374A2.813 2.813 0 0 0 7.813 43h24.375A2.813 2.813 0 0 0 35 40.187V15.814A2.813 2.813 0 0 0 32.187 13Z" />
                </svg>
              )}
            </button>
          </div>
          {isConverting && (
            <div className="processing-state" role="status" aria-live="polite">
              <div className="progress-track">
                <div className="progress-bar" />
              </div>
              <span className="processing-label">
                <svg aria-hidden="true" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="9" />
                </svg>
                Processing
              </span>
            </div>
          )}
          <textarea
            value={markdown}
            readOnly
            spellCheck={false}
            placeholder="Your converted Markdown will appear here..."
          />
        </section>
      )}
    </main>
  );
}

export default App;
