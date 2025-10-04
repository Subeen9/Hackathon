"use client";
import { Document, Page, pdfjs } from "react-pdf";
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

export default function PdfViewer({ fileUrl }: { fileUrl: string }) {
  if (!fileUrl) return null;

  return (
    <Document file={fileUrl}>
      <Page pageNumber={1} width={400} />
    </Document>
  );
}
