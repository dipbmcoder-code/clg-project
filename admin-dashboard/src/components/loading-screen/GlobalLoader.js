import React from "react";
import { Backdrop, CircularProgress } from "@mui/material";

function GlobalLoader({ open }) {
  return (
    <Backdrop
      sx={{
        color: "#fff",
        backgroundColor: "rgba(0, 0, 0, 0.3)",
        zIndex: (theme) => theme.zIndex.drawer + 9999, // make sure it's above everything
      }}
      open={open}
    >
      <CircularProgress color="inherit" />
    </Backdrop>
  );
}

export default GlobalLoader;
