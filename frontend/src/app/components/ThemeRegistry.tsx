"use client";

import { ReactNode } from "react";
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#c9b2a0" },   // light brown (Navbar/Footer)
    secondary: { main: "#8b5e3c" }, // darker accent brown
    background: {
      default: "#faecd8", // parchment base
      paper: "#fffef8",   // cards/panels
    },
    text: {
      primary: "#3e2f1c",
      secondary: "#5a4630",
    },
  },
  typography: {
    fontFamily: `"Geist", "Geist Mono", sans-serif`,
  },
});

export default function ThemeRegistry({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
