"use client";
import { useEffect, useState } from "react";
import { Typography, Paper, Box } from "@mui/material";
import Grid from "@mui/material/Grid";
import dynamic from "next/dynamic";

// Import PdfViewer dynamically to disable SSR
const PdfViewer = dynamic(() => import("../components/PdfViewer"), {
  ssr: false,
});

export default function ViewerPage() {
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [translation, setTranslation] = useState<string>("");

  useEffect(() => {
    const url = localStorage.getItem("uploadedFileUrl");
    console.log("Retrieved fileUrl:", url); // Debug log
    if (url) {
      setFileUrl(url);
      setTranslation(
        "Mock translation: This is where the AI-generated translation will appear."
      );
    }
  }, []);

  return (
    <Grid container spacing={2} sx={{ height: "calc(100vh - 64px)", p: 2 }}>
      {/* Original Document */}
      <Grid size={{ xs: 12, md: 6 }}>
        <Paper sx={{ height: "100%", p: 2, backgroundColor: "background.paper" }}>
          <Typography
            variant="h6"
            gutterBottom
            sx={{ borderBottom: "2px solid", borderColor: "primary.main", pb: 1 }}
          >
            Original Document
          </Typography>
          <Box
            sx={{
              height: "90%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              overflow: "auto",
            }}
          >
            {!fileUrl ? (
              <Typography color="text.secondary">No document uploaded</Typography>
            ) : fileUrl.endsWith(".pdf") ? (
              <PdfViewer fileUrl={fileUrl} />
            ) : (
              <Box
                sx={{
                  height: "100%",
                  width: "100%",
                  overflow: "auto",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <img
                  src={fileUrl}
                  alt="Uploaded file"
                  style={{
                    width: "100%",
                    height: "auto",
                    borderRadius: "8px",
                  }}
                />
              </Box>
            )}
          </Box>
        </Paper>
      </Grid>

      {/* Translated Text */}
      <Grid size={{ xs: 12, md: 6 }}>
        <Paper sx={{ height: "100%", p: 2, backgroundColor: "background.paper" }}>
          <Typography
            variant="h6"
            gutterBottom
            sx={{ borderBottom: "2px solid", borderColor: "primary.main", pb: 1 }}
          >
            Translated Text
          </Typography>
          <Box sx={{ height: "90%", overflowY: "auto", p: 2 }}>
            {translation ? (
              <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                {translation}
              </Typography>
            ) : (
              <Typography color="text.secondary">
                Translation will appear here
              </Typography>
            )}
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
}
