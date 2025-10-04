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
  Tooltip,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import dynamic from "next/dynamic";
import TranslateIcon from "@mui/icons-material/Translate";
import VolumeUpIcon from "@mui/icons-material/VolumeUp";
import UndoIcon from "@mui/icons-material/Undo";

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

  //  Dummy glossary (replace with backend later)
  const glossary: Record<string, string> = {
    mock: "A simulated or artificial example used for demonstration.",
    translation: "The process of converting text from one language to another.",
    digitalized: "Converted into a digital form that can be processed by computers.",
    original: "The first or earliest form of something.",
    replaced: "Substituted or taken the place of something else.",
  };

  useEffect(() => {
    const url = localStorage.getItem("uploadedFileUrl");
    const text = localStorage.getItem("processedText");
    const raw = localStorage.getItem("rawText");

    console.log("Retrieved from localStorage:", { url, text, raw });

    if (url) setFileUrl(url);
    if (text) setProcessedText(text);
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

  //  Function to render words with tooltips
  const renderTranslatedText = (text: string) => {
    const words = text.split(" ");
    return words.map((word, idx) => {
      const cleanWord = word.replace(/[.,!?]/g, "").toLowerCase();
      const meaning = glossary[cleanWord];
      if (meaning) {
        return (
          <Tooltip
            key={idx}
            title={meaning}
            arrow
            placement="top"
            slotProps={{
              popper: { modifiers: [{ name: "offset", options: { offset: [0, 8] } }] },
            }}
            componentsProps={{
              tooltip: {
                sx: {
                  bgcolor: "#8b5e3c",
                  color: "#fffef8",
                  fontSize: "0.85rem",
                  borderRadius: "8px",
                  px: 1.5,
                  py: 0.5,
                  boxShadow: "0 2px 10px rgba(0,0,0,0.25)",
                },
              },
            }}
          >
            <span
              style={{
                cursor: "help",
                fontWeight: 600,
                color: "#8b5e3c",
                transition: "background-color 0.2s ease",
              }}
            >
              {word + " "}
            </span>
          </Tooltip>
        );
      }
      return word + " ";
    });
  };

  return (
    <Grid container spacing={2} sx={{ height: "calc(100vh - 64px)", p: 2 }}>
      {/* Original Document */}
      <Grid size={{ xs: 12, md: 6 }}>
        <Paper
          elevation={3}
          sx={{
            height: "100%",
            p: 2,
            display: "flex",
            flexDirection: "column",
          }}
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
          sx={{
            height: "100%",
            p: 2,
            display: "flex",
            flexDirection: "column",
          }}
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
                {englishTranslation
                  ? renderTranslatedText(englishTranslation)
                  : processedText}
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
