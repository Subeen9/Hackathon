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
import Grid from "@mui/material/Grid"; // Updated import
import dynamic from "next/dynamic";
import TranslateIcon from "@mui/icons-material/Translate";
import VolumeUpIcon from "@mui/icons-material/VolumeUp";
import UndoIcon from "@mui/icons-material/Undo";

const PdfViewer = dynamic(() => import("../components/PdfViewer"), {
  ssr: false,
});

export default function ViewerPage() {
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [processedText, setProcessedText] = useState<string>("");
  const [englishTranslation, setEnglishTranslation] = useState<string>("");
  const [isTranslating, setIsTranslating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [lemmaData, setLemmaData] = useState<any[]>([]);

  useEffect(() => {
    const url = localStorage.getItem("uploadedFileUrl");
    const text = localStorage.getItem("processedText");
    const lemma = localStorage.getItem("LemmaText");

    console.log("Retrieved from localStorage:", { url, text, lemma });

    if (url) setFileUrl(url);
    if (text) setProcessedText(text);

    if (lemma) {
      try {
        const parsed = JSON.parse(lemma);
        setLemmaData(parsed);
        console.log("Parsed Lemma:", parsed);
      } catch (err) {
        console.error("Invalid LemmaText JSON:", err);
      }
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

  const handleRevert = () => {
    setEnglishTranslation("");
  };

  const handleSpeak = () => {
    const textToSpeak = englishTranslation || processedText;
    if (!textToSpeak || isSpeaking) return;

    setIsSpeaking(true);
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.onend = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
    } else {
      console.log("Mocking speech for:", textToSpeak);
      setTimeout(() => setIsSpeaking(false), 3000);
    }
  };

  const renderLemmaText = () => {
    if (!lemmaData?.length) return processedText;

    return lemmaData.map((item, idx) => (
      <Tooltip
        key={idx}
        title={
          <Box>
            <Typography variant="caption" display="block">
              <strong>Lemma:</strong> {item.lemma || "N/A"}
            </Typography>
            <Typography variant="caption" display="block">
              <strong>POS:</strong> {item.pos_description || item.pos || "unknown"}
            </Typography>
          </Box>
        }
        arrow
        placement="top"
        slotProps={{
          tooltip: {
            sx: {
              bgcolor: "#8b5e3c",
              color: "#fffef8",
              fontSize: "0.85rem",
              borderRadius: "8px",
              px: 1.5,
              py: 1,
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
            marginRight: "4px",
            display: "inline-block",
          }}
        >
          {item.word}
        </span>
      </Tooltip>
    ));
  };

  return (
    <Grid container spacing={2} sx={{ height: "calc(100vh - 64px)", p: 2 }}>
      {/* Original Document - LEFT SIDE */}
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

      {/* Digitalized & Translated Text - RIGHT SIDE */}
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

          {/* Text with lemma tooltips */}
          <Box sx={{ flexGrow: 1, overflowY: "auto", p: 1 }}>
            {englishTranslation ? (
              <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                {englishTranslation}
              </Typography>
            ) : processedText ? (
              <Typography 
                component="div"
                variant="body1" 
                sx={{ 
                  whiteSpace: "normal", 
                  lineHeight: 1.8,
                  wordWrap: "break-word"
                }}
              >
                {renderLemmaText()}
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