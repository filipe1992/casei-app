import React from "react";
import { Container, Typography, Card, Grid } from "@mui/material";
import { Camera } from "@mui/icons-material";

const photoItens = [
    { id: "album", label: "Album de Fotos", icon: <Camera />, description: "Fotos compartilhadas e desafios fotográficos." },
    { id: "album", label: "Album de fotos do convidado fulano", icon: <Camera />, description: "Fotos compartilhadas pelo convidado fulano" },
    { id: "album", label: "Album de fotos do convidado ciclano", icon: <Camera />, description: "Fotos compartilhadas pelo convidado ciclano" },
    { id: "album", label: "Album de fotos do convidado beltrano", icon: <Camera />, description: "Fotos compartilhadas pelo convidado beltrano" },
];

const PhotosPage = () => {
    return (
        <Container maxWidth="lg" sx={{ mt: 4, px: 3 }}>
            <Typography variant="h4" sx={{ fontWeight: "bold", color: "#111827", mb: 2, textAlign: { xs: "center", sm: "left" } }}>
                Álbum de Fotos
            </Typography>
            <Typography variant="body1" sx={{ color: "#6b7280", mb: 3, textAlign: { xs: "center", sm: "left" } }}>
                Fotos compartilhadas e desafios fotográficos.
            </Typography>

            <Grid container spacing={5} gridRow={2} gridColumn={2} sx={{ display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
                {photoItens.map(({ id, label, icon, description }) => (
                    <Grid item xs={12} sm={6} md={3} key={id}>
                        <Card sx={{
                            backgroundColor: "white",
                            borderRadius: 2,
                            border: "1px solid #e5e7eb",
                            boxShadow: 1,
                            p: { xs: 2, sm: 3 },
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            textAlign: "center"
                        }}>
                            {icon}
                            <Typography variant="h6" sx={{ fontWeight: 500, mb: 1 }}>
                                {label}
                            </Typography>
                            <Typography variant="body2" sx={{ maxWidth: 400 }}>
                                {description}
                            </Typography>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Container>
    );
};

export default PhotosPage;
