"use client";

import { ReactNode } from "react";
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#367583" },   // Navbar & Footer color
    secondary: { main: "#2b5c66" }, // slightly darker shade for accents
    background: {
      default: "#0d1117", // dark page background
      paper: "#161b22",   // cards / panels
    },
    text: {
      primary: "#e0f2f1",   // light text
      secondary: "#b2dfdb", // muted teal text
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
