import { useEffect, useRef, useState } from "react";

type Language = "en" | "es" | "ca";
type RecognitionType = "page" | "text_formula" | "formula" | "text";
type ApiResponse = { markdown?: string; detail?: unknown };

const recognitionOptions: Array<{ value: RecognitionType; label: string }> = [
  { value: "page", label: "Pàgina" },
  { value: "text_formula", label: "Text i fórmules" },
  { value: "formula", label: "Fórmula" },
  { value: "text", label: "Text" },
];

function formatError(detail: unknown): string {
  if (typeof detail === "string" && detail) return detail;
  if (detail instanceof Error) return detail.message;
  if (detail !== undefined) {
    try {
      return JSON.stringify(detail);
    } catch {
      return "La conversió ha fallat.";
    }
  }
  return "La conversió ha fallat.";
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File>();
  const [language, setLanguage] = useState<Language>("ca");
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
      setMessage("Selecciona una imatge.");
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
      setMessage("Enganxa o selecciona una imatge primer.");
      return;
    }

    const data = new FormData();
    data.append("image", file);
    data.append("language", language);
    data.append("recognition_type", recognitionType);
    setIsConverting(true);
    setMessage("");

    try {
      const response = await fetch("/api/convert", {
        method: "POST",
        body: data,
      });
      let body: ApiResponse;
      try {
        body = (await response.json()) as ApiResponse;
      } catch {
        throw new Error(`La conversió ha fallat (${response.status}).`);
      }
      if (!response.ok) throw new Error(formatError(body.detail));
      setMarkdown(body.markdown ?? "");
      setMessage("");
    } catch (reason) {
      setMessage(reason instanceof Error ? reason.message : "La conversió ha fallat.");
    } finally {
      setIsConverting(false);
    }
  };

  const copyMarkdown = async () => {
    await navigator.clipboard.writeText(markdown);
  };

  return (
    <main className="app-shell">
      <div className="app-content">
      <label className="field-label" htmlFor="language">Idioma</label>
        <select
          id="language"
          className="select"
          value={language}
          onChange={(event) => setLanguage(event.target.value as Language)}
        >
            <option value="en">Anglès</option>
            <option value="es">Castellà</option>
            <option value="ca">Català</option>
        </select>

        <label className="field-label" htmlFor="recognition-type">Tipus de reconeixement</label>
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
        <strong>Arrossega o enganxa una imatge, o clica per seleccionar-la</strong>
        <span className="drop-help">(Admet arrossegar, Ctrl+V i fitxers d'imatge)</span>
        {previewUrl && <img className="preview" src={previewUrl} alt="Previsualització" />}
      </button>
      <input
        ref={fileInput}
        className="file-input"
        type="file"
        accept="image/*"
        onChange={(event) => setFile(event.target.files?.[0])}
      />
      {message && <p className="message" role="alert">{message}</p>}
      {selectedFile && (
        <section className="result-card">
          <div className="result-header">
            <span>Resultat</span>
            <button
              className={`copy-button${copied ? " copied" : ""}`}
              type="button"
              onClick={async () => {
                await copyMarkdown();
                setCopied(true);
                window.setTimeout(() => setCopied(false), 1200);
              }}
              disabled={!markdown}
              aria-label={copied ? "Markdown copiat" : "Copia el Markdown"}
              title={copied ? "Copiat" : "Copia el Markdown"}
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
                Processant
              </span>
            </div>
          )}
          <textarea
            value={markdown}
            readOnly
            spellCheck={false}
            placeholder="El Markdown convertit apareixerà aquí..."
          />
        </section>
      )}
      <footer className="source-footer">
        <h3>Codi font</h3>
        <p>
          GitHub:{" "}
          <a href="https://github.com/Mapaor/pix2text-ocr-cat" target="_blank" rel="noreferrer">
            pix2text-ocr-cat
          </a>
          &nbsp;(basat en <a href="https://github.com/breezedeus/Pix2Text" target="_blank" rel="noreferrer">
            pix2tex
          </a>)
        </p>
        <p className="source-note">
          Nota: Per text normal utilitza{" "}
          <a href="https://ocr.cat/" target="_blank" rel="noreferrer">
            ocr.cat
          </a>
        </p>
      </footer>
      </div>
    </main>
  );
}

export default App;
