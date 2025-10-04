"use client";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export default function PdfViewer({ fileUrl }: { fileUrl: string }) {
  if (!fileUrl) return null;

  return (
    <Document file={fileUrl}>
      <Page pageNumber={1} width={400} />
    </Document>
  );
}
