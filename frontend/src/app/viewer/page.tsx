"use client";
import { Typography, Paper, Box } from "@mui/material";
import Grid from "@mui/material/Grid"; // ✅ Correct import

export default function ViewerPage() {
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
            <Typography color="text.secondary">[Preview will show here]</Typography>
          </Box>
        </Paper>
      </Grid>

      {/* Translated Document */}
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
            <Typography variant="body1">
              [Translated text will appear here]
            </Typography>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
}
