import React from "react";
import { Container, Typography, Card, Grid, Box } from "@mui/material";
import { Settings, Tune, Security, Palette } from "@mui/icons-material";

const settingsItems = [
  { id: "system", label: "Configurações do Sistema", icon: <Settings />, description: "Ajuste as preferências do seu casamento." },
  { id: "appearance", label: "Personalização", icon: <Palette />, description: "Escolha temas e estilos visuais para seu evento." },
  { id: "privacy", label: "Segurança e Privacidade", icon: <Security />, description: "Gerencie quem pode ver e interagir com seu conteúdo." },
  { id: "advanced", label: "Configurações Avançadas", icon: <Tune />, description: "Acesse opções detalhadas e ajustes técnicos." },
];

const SettingsPage = () => {
  return (
    <Container maxWidth="lg" maxHeight="lg" sx={{ mt: 4, px: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: "bold", color: "#111827", mb: 2, textAlign: { xs: "center", sm: "left" } }}>
        Configurações
      </Typography>
      <Typography variant="body1" sx={{ color: "#6b7280", mb: 3, textAlign: { xs: "center", sm: "left" } }}>
        Personalize as configurações do seu evento de maneira detalhada e intuitiva.
      </Typography>

      <Grid container spacing={5} sx={{ display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
        {settingsItems.map(({ id, label, icon, description }) => (
          <Grid item xs={12} sm={6} md={3} key={id} sx={{ display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
            <Card sx={{ p: 3, textAlign: "center", border: "1px solid #e5e7eb", boxShadow: 1 }}>
              <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
                {icon}
              </Box>
              <Typography variant="h6" sx={{ fontWeight: 500, mb: 1 }}>
                {label}
              </Typography>
              <Typography variant="body2" sx={{ color: "#6b7280" }}>
                {description}
              </Typography>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default SettingsPage;
