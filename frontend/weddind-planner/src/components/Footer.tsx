import React from "react";
import { Box, Typography, Container } from "@mui/material";

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: "#f9fafb",
        borderTop: "1px solid #e5e7eb",
        py: 3,
        mt: 4,
      }}
    >
      <Container maxWidth="lg" sx={{ textAlign: "center" }}>
        <Typography variant="body2" color="textSecondary">
          © {new Date().getFullYear()} CasaFácil - Todos os direitos reservados.
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Feito com ❤️ para tornar seu casamento ainda mais especial.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
