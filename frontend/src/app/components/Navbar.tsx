"use client";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";

export default function Navbar() {
  return (
    <AppBar
      position="sticky"
      elevation={3}
      sx={{ backgroundColor: "primary.main" }}  // Force #367583
    >
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          Texti-Fy
        </Typography>
        <div>
          <Button color="inherit" href="/">Home</Button>
          <Button color="inherit" href="/viewer">Viewer</Button>
        </div>
      </Toolbar>
    </AppBar>
  );
}
