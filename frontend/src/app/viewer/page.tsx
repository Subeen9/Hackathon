"use client";
import { useEffect, useState } from "react";
import {
  Typography,
  Paper,
  Box,
  Button,
  Stack,
  IconButton,
  CircularProgress,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import dynamic from "next/dynamic";
import TranslateIcon from "@mui/icons-material/Translate";
import VolumeUpIcon from "@mui/icons-material/VolumeUp";
import UndoIcon from "@mui/icons-material/Undo"; // Import the new icon

// Import PdfViewer dynamically to disable SSR
const PdfViewer = dynamic(() => import("../components/PdfViewer"), {
  ssr: false,
});

export default function ViewerPage() {
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [processedText, setProcessedText] = useState<string>("");
  const [englishTranslation, setEnglishTranslation] = useState<string>("");
  const [isTranslating, setIsTranslating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [rawText, setRawText] = useState<string>("");

  useEffect(() => {
    const url = localStorage.getItem("uploadedFileUrl");
    const text = localStorage.getItem("processedText");
    const raw = localStorage.getItem("rawText");
    
    console.log("Retrieved from localStorage:", { url, text, raw }); 
    
    if (url) {
      setFileUrl(url);
    }
    if (text) {
      setProcessedText(text);
    }
  }, []);
  useEffect(() => {
    const url = localStorage.getItem("uploadedFileUrl");
    if (url) {
      setFileUrl(url);
      setProcessedText(
        "This is the initial digitalized text from the document. It appears here first, ready to be translated or read aloud."
      );
    }
  }, []);

  const handleTranslate = () => {
    setIsTranslating(true);
    setTimeout(() => {
      setEnglishTranslation(
        "This is the mock English translation of the text. It has now replaced the original digitalized text."
      );
      setIsTranslating(false);
    }, 1500);
  };

  // New function to revert to the original text
  const handleRevert = () => {
    setEnglishTranslation("");
  };

  const handleSpeak = () => {
    const textToSpeak = englishTranslation || processedText;
    if (!textToSpeak || isSpeaking) return;

    setIsSpeaking(true);
    console.log("Mocking speech for:", textToSpeak);
    setTimeout(() => {
      setIsSpeaking(false);
    }, 3000);
  };

  return (
    <Grid container spacing={2} sx={{ height: "calc(100vh - 64px)", p: 2 }}>
      {/* Original Document */}
      <Grid size={{ xs: 12, md: 6 }}>
        <Paper
          elevation={3}
          sx={{ height: "100%", p: 2, display: "flex", flexDirection: "column" }}
        >
          <Typography
            variant="h6"
            gutterBottom
            sx={{ borderBottom: "2px solid", borderColor: "primary.main", pb: 1 }}
          >
            Original Document
          </Typography>
          <Box
            sx={{
              flexGrow: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              overflow: "auto",
              minHeight: 0,
            }}
          >
            {!fileUrl ? (
              <Typography color="text.secondary">No document uploaded</Typography>
            ) : fileUrl.endsWith(".pdf") ? (
              <PdfViewer fileUrl={fileUrl} />
            ) : (
              <Box
                component="img"
                src={fileUrl}
                alt="Uploaded document"
                sx={{
                  maxWidth: "100%",
                  maxHeight: "100%",
                  objectFit: "contain",
                  borderRadius: "8px",
                }}
              />
            )}
          </Box>
        </Paper>
      </Grid>

      {/* Digitalized & Translated Text */}
      <Grid size={{ xs: 12, md: 6 }}>
        <Paper
          elevation={3}
          sx={{ height: "100%", p: 2, display: "flex", flexDirection: "column" }}
        >
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              borderBottom: "2px solid",
              borderColor: "primary.main",
              pb: 1,
              mb: 2,
            }}
          >
            <Typography variant="h6">
              {englishTranslation ? "Translated Text" : "Digitalized Text"}
            </Typography>
            <Stack direction="row" spacing={1}>
              {/*  This block now conditionally shows Translate or Revert */}
              {englishTranslation ? (
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<UndoIcon />}
                  onClick={handleRevert}
                >
                  Show Original
                </Button>
              ) : (
                <Button
                  variant="contained"
                  size="small"
                  startIcon={
                    isTranslating ? (
                      <CircularProgress size={20} color="inherit" />
                    ) : (
                      <TranslateIcon />
                    )
                  }
                  onClick={handleTranslate}
                  disabled={!processedText || isTranslating}
                >
                  Translate
                </Button>
              )}
              <IconButton
                onClick={handleSpeak}
                disabled={(!processedText && !englishTranslation) || isSpeaking}
                color="primary"
                aria-label="speak text"
              >
                <VolumeUpIcon />
              </IconButton>
            </Stack>
          </Box>
          <Box sx={{ flexGrow: 1, overflowY: "auto", p: 1 }}>
            {processedText || englishTranslation ? (
              <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                {englishTranslation || processedText}
              </Typography>
            ) : (
              <Typography color="text.secondary">
                Text will appear here after processing.
              </Typography>
            )}
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
}