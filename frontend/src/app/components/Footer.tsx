"use client";
import { Box, Container, Typography, Divider } from "@mui/material";

export default function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: "primary.main",
        color: "black",
        mt: 6,
        pt: 6,
        pb: 3,
      }}
    >
      <Container maxWidth="md" sx={{ textAlign: "center" }}>
        {/* Branding */}
        <Typography variant="h6" fontWeight="bold" gutterBottom>
          Texti-Fy
        </Typography>
        <Typography variant="body2" sx={{ maxWidth: 500, mx: "auto", mb: 2 }}>
          Unlocking the wisdom of ancient manuscripts with modern AI.
        </Typography>

        {/* Divider */}
        <Divider
          sx={{
            backgroundColor: "rgba(255,255,255,0.2)",
            my: 2,
            mx: "auto",
            width: "60%",
          }}
        />

        {/* Bottom Bar */}
        <Typography variant="body2" sx={{ opacity: 0.8 }}>
          © {new Date().getFullYear()} Texti-Fy · Built at HackHarvard 
        </Typography>
      </Container>
    </Box>
  );
}
