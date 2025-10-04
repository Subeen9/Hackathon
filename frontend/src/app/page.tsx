"use client";
import { useState, useCallback, useRef } from "react";
import { useDropzone } from "react-dropzone";
import {
  Container,
  Typography,
  Button,
  Paper,
  Box,
  LinearProgress,
  FormControl,
  InputLabel,
  Modal,
  Select,
  MenuItem,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CameraAltIcon from "@mui/icons-material/CameraAlt";
import Webcam from "react-webcam";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [openCamera, setOpenCamera] = useState(false);
  const webcamRef = useRef<Webcam>(null);
  const [language, setLanguage] = useState("latin");


  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) setFile(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
    },
  });

  const capturePhoto = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      const blob = dataURLtoBlob(imageSrc);
      const capturedFile = new File([blob], "capture.jpg", {
        type: "image/jpeg",
      });
      setFile(capturedFile);
      setOpenCamera(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language);
    try {
      setUploading(true);
      const res = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();

      console.log("Upload response:", data); // Debug log


      localStorage.setItem("uploadedFileUrl", data.file_url);  // Changed from data.url
      localStorage.setItem("processedText", data.accurate_text);
      localStorage.setItem("rawText", data.raw_ocr_text);
      localStorage.setItem("language", data.language);

      setTimeout(() => (window.location.href = "/viewer"), 1000);
    } catch (err) {
      console.error("Upload error:", err);
      setUploading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#faecd8",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundImage:
          "radial-gradient(#f5e7cf 1px, transparent 1px), radial-gradient(#f5e7cf 1px, transparent 1px)",
        backgroundSize: "20px 20px",
        backgroundPosition: "0 0, 10px 10px",
      }}
    >
      <Container
        maxWidth="md"
        sx={{
          textAlign: "center",
          py: 6,
          backgroundColor: "#fffef8",
          borderRadius: "16px",
          boxShadow: "0 8px 24px rgba(139, 94, 60, 0.25)",
          border: "1px dashed #d2b48c",
        }}
      >
        <Typography
          variant="h4"
          gutterBottom
          sx={{ color: "#3e2f1c", fontWeight: 700 }}
        >
          Uncover the Past
        </Typography>
        <Typography
          variant="body1"
          sx={{
            mb: 4,
            color: "#5a4630",
            maxWidth: "90%",
            mx: "auto",
            fontSize: "1.05rem",
          }}
        >
          Drag & Drop your manuscript PDF or image below — or capture one
          directly using your camera.
        </Typography>

        <FormControl
          fullWidth
          sx={{
            mb: 3,
            maxWidth: "400px",
            mx: "auto",
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                borderColor: "#c49a6c",
              },
              "&:hover fieldset": {
                borderColor: "#8b5e3c",
              },
              "&.Mui-focused fieldset": {
                borderColor: "#8b5e3c",
              },
            },
          }}
        >
          <InputLabel sx={{ color: "#5a4630" }}>Manuscript Language</InputLabel>
          <Select
            value={language}
            label="Manuscript Language"
            onChange={(e) => setLanguage(e.target.value)}
            sx={{
              bgcolor: "#fffef8",
              color: "#3e2f1c",
              borderRadius: "8px",
            }}
          >
            <MenuItem value="latin">Latin</MenuItem>
            <MenuItem value="old_english">Old English</MenuItem>
            <MenuItem value="sanskrit">Sanskrit </MenuItem>
          </Select>
        </FormControl>
        <Paper
          {...getRootProps()}
          elevation={3}
          sx={{
            border: "2px dashed #c49a6c",
            backgroundColor: isDragActive ? "#f8e8c6" : "#fffef8",
            color: "#3e2f1c",
            borderRadius: "12px",
            p: 6,
            mb: 3,
            cursor: "pointer",
            textAlign: "center",
            transition: "all 0.3s ease",
            "&:hover": {
              borderColor: "#8b5e3c",
              backgroundColor: "#faf0db",
            },
          }}
        >
          <input {...getInputProps()} />
          <CloudUploadIcon sx={{ fontSize: 60, color: "#8b5e3c", mb: 2 }} />
          {file ? (
            <Typography variant="subtitle1" sx={{ color: "#8b5e3c" }}>
              {file.name}
            </Typography>
          ) : isDragActive ? (
            <Typography variant="subtitle1" sx={{ color: "#8b5e3c" }}>
              Drop the file here…
            </Typography>
          ) : (
            <Typography variant="subtitle1" sx={{ color: "#3e2f1c" }}>
              Drag & drop a file here, or click to select
            </Typography>
          )}
        </Paper>

        {/* CAMERA + UPLOAD BUTTONS ROW */}
        {uploading ? (
          <Box display="flex" flexDirection="column" alignItems="center" mt={2}>
            <Typography variant="body2" sx={{ mb: 1, color: "#8b5e3c" }}>
              Uploading your manuscript...
            </Typography>
            <LinearProgress
              sx={{
                width: "100%",
                "& .MuiLinearProgress-bar": {
                  backgroundColor: "#8b5e3c",
                },
              }}
            />
          </Box>
        ) : (
          <Box
            sx={{
              mt: 3,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: 2,
            }}
          >
            <Button
              variant="outlined"
              startIcon={<CameraAltIcon />}
              onClick={() => setOpenCamera(true)}
              sx={{
                borderColor: "#8b5e3c",
                color: "#8b5e3c",
                "&:hover": {
                  bgcolor: "#faf0db",
                  borderColor: "#8b5e3c",
                },
                minWidth: "180px",
                py: 1.2,
              }}
            >
              Open Camera
            </Button>

            <Button
              variant="contained"
              size="large"
              onClick={handleUpload}
              disabled={!file}
              sx={{
                bgcolor: "#8b5e3c",
                "&:hover": { bgcolor: "#714a30" },
                color: "#fffef8",
                fontWeight: 600,
                textTransform: "none",
                borderRadius: "8px",
                px: 4,
                py: 1.2,
                minWidth: "180px",
                boxShadow: "0 4px 10px rgba(139, 94, 60, 0.3)",
                "&.Mui-disabled": {
                  bgcolor: "#d6c1aa",
                  color: "#fffef8",
                  opacity: 0.8,
                },
              }}
            >
              Upload & Process
            </Button>
          </Box>
        )}
      </Container>

      {/* CAMERA MODAL */}
      <Modal
        open={openCamera}
        onClose={() => setOpenCamera(false)}
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Box
          sx={{
            backgroundColor: "#fffef8",
            borderRadius: "12px",
            p: 3,
            boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
            border: "2px solid #c49a6c",
            textAlign: "center",
          }}
        >
          <Typography variant="h6" sx={{ mb: 2, color: "#3e2f1c" }}>
            Capture Manuscript
          </Typography>
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            style={{
              width: "100%",
              maxWidth: 480,
              borderRadius: "8px",
              border: "2px solid #c49a6c",
            }}
          />
          <Box sx={{ mt: 2, display: "flex", gap: 2, justifyContent: "center" }}>
            <Button
              variant="contained"
              onClick={capturePhoto}
              sx={{
                bgcolor: "#8b5e3c",
                "&:hover": { bgcolor: "#714a30" },
                color: "#fffef8",
              }}
            >
              Capture
            </Button>
            <Button
              variant="outlined"
              onClick={() => setOpenCamera(false)}
              sx={{
                borderColor: "#8b5e3c",
                color: "#8b5e3c",
                "&:hover": { bgcolor: "#faf0db" },
              }}
            >
              Cancel
            </Button>
          </Box>
        </Box>
      </Modal>
    </Box>
  );
}

/* helper */
function dataURLtoBlob(dataURL: string) {
  const arr = dataURL.split(",");
  const mime = arr[0].match(/:(.*?);/)![1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) u8arr[n] = bstr.charCodeAt(n);
  return new Blob([u8arr], { type: mime });
}
