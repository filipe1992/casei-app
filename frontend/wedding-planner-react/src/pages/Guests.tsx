import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  TextField,
  TablePagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  InputAdornment,
  CircularProgress,
  Button,
  Tooltip,
  IconButton,
  Menu,
  ListItemIcon,
} from '@mui/material';
import GroupIcon from '@mui/icons-material/Group';
import SearchIcon from '@mui/icons-material/Search';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PendingIcon from '@mui/icons-material/Pending';
import AddIcon from '@mui/icons-material/Add';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import TaskAltIcon from '@mui/icons-material/TaskAlt';
import SendIcon from '@mui/icons-material/Send';
import { Guest } from '../types/guest.ts';
import { useGuests } from '../hooks/useGuests.ts';
import AddGuestDialog from '../components/guests/AddGuestDialog.tsx';
import EditGuestDialog from '../components/guests/EditGuestDialog.tsx';
import ConfirmDeleteDialog from '../components/guests/ConfirmDeleteDialog.tsx';

const GuestActionsMenu = ({ guest, onEdit, onDelete, onConfirmToggle }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => setAnchorEl(event.currentTarget);
  const handleClose = () => setAnchorEl(null);

  const handleEdit = () => {
    onEdit(guest);
    handleClose();
  };

  const handleDelete = () => {
    onDelete(guest);
    handleClose();
  };

  const handleConfirmToggle = () => {
    onConfirmToggle(guest.id, { confirmed: !guest.confirmed });
    handleClose();
  };

  return (
    <>
      <IconButton onClick={handleClick}>
        <MoreVertIcon />
      </IconButton>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem onClick={handleEdit}>
          <ListItemIcon><EditIcon fontSize="small" /></ListItemIcon>
          Editar
        </MenuItem>
        <MenuItem onClick={handleDelete} sx={{ color: 'error.main' }}>
          <ListItemIcon><DeleteIcon fontSize="small" color="error" /></ListItemIcon>
          Deletar
        </MenuItem>
        <MenuItem onClick={handleConfirmToggle}>
          <ListItemIcon><TaskAltIcon fontSize="small" /></ListItemIcon>
          {guest.confirmed ? 'Marcar como Pendente' : 'Confirmar Presença'}
        </MenuItem>
      </Menu>
    </>
  );
}

const Guests: React.FC = () => {
  const {
    page,
    rowsPerPage,
    searchTerm,
    statusFilter,
    loading,
    filteredGuests,
    statistics,
    handleChangePage,
    handleChangeRowsPerPage,
    handleSearchChange,
    handleStatusChange,
    isAddGuestDialogOpen,
    handleOpenAddDialog,
    handleCloseAddDialog,
    handleAddGuest,
    isEditGuestDialogOpen,
    handleOpenEditDialog,
    handleCloseEditDialog,
    isDeleteConfirmOpen,
    handleOpenDeleteDialog,
    handleCloseDeleteDialog,
    selectedGuest,
    handleUpdateGuest,
    handleDeleteGuest,
    handleSendPendingInvitations
  } = useGuests();

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 'bold', color: 'primary.main' }}>
        Dashboard de Convidados
      </Typography>

      <Grid container spacing={4} sx={{ mb: 6 }}>
        <Grid>
          <Card sx={{
            height: '100%',
            backgroundColor: '#f5f5f5',
            borderRadius: 2,
            boxShadow: 3,
            transition: 'transform 0.2s',
            '&:hover': { transform: 'scale(1.02)' }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <GroupIcon fontSize="large" color="primary" />
                <Typography color="textSecondary" variant="h6">
                  Total
                </Typography>
              </Box>
              <Typography
                variant="h2"
                sx={{
                  fontWeight: 'bold',
                  mt: 3,
                  textAlign: 'center',
                  color: 'primary.main'
                }}
              >
                {statistics?.total_guests}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid >
          <Card sx={{
            height: '100%',
            backgroundColor: '#f5f5f5',
            borderRadius: 2,
            boxShadow: 3,
            transition: 'transform 0.2s',
            '&:hover': { transform: 'scale(1.02)' }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <GroupIcon fontSize="large" color="primary" />
                <Typography color="textSecondary" variant="h6">
                  Taxa de Confirmação
                </Typography>
              </Box>
              {(() => {
                const confirmationRate = statistics?.percentage_confirmed_guests || 0;
                const color = confirmationRate >= 90 
                  ? 'success.main'
                  : confirmationRate >= 70 
                    ? 'warning.main' 
                    : 'error.main';
                
                return (
                  <Typography
                    variant="h2"
                    sx={{
                      fontWeight: 'bold',
                      mt: 3,
                      textAlign: 'center',
                      color: color
                    }}
                  >
                    {confirmationRate.toFixed(1)}%
                  </Typography>
                );
              })()}
            </CardContent>
          </Card>
        </Grid>

        <Grid >
          <Card sx={{
            height: '100%',
            backgroundColor: '#e8f5e9',
            borderRadius: 2,
            boxShadow: 3,
            transition: 'transform 0.2s',
            '&:hover': { transform: 'scale(1.02)' }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <GroupIcon fontSize="large" color="success" />
                <Typography color="textSecondary" variant="h6">
                  Confirmados
                </Typography>
              </Box>
              <Typography
                variant="h2"
                sx={{
                  fontWeight: 'bold',
                  mt: 3,
                  textAlign: 'center',
                  color: 'success.main'
                }}
              >{statistics?.total_confirmed_guests}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid >
          <Card sx={{
            height: '100%',
            backgroundColor: '#ffcdd2',
            borderRadius: 2,
            boxShadow: 3,
            transition: 'transform 0.2s',
            '&:hover': { transform: 'scale(1.02)' }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <GroupIcon fontSize="large" color="error" />
                <Typography color="textSecondary" variant="h6">
                  Não Confirmados
                </Typography>
              </Box>
              <Typography
                variant="h2"
                sx={{
                  fontWeight: 'bold',
                  mt: 3,
                  textAlign: 'center',
                  color: 'error.main'
                }}
              >{statistics?.total_unconfirmed_guests}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      

      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', flexGrow: 1 }}>
          <TextField
            placeholder="Buscar por nome ou telefone"
            variant="outlined"
            size="small"
            value={searchTerm}
            onChange={handleSearchChange}
            sx={{ flexGrow: 1, minWidth: '200px' }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="action" />
                </InputAdornment>
              ),
            }}
          />
          <FormControl size="small" sx={{ minWidth: '150px' }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              label="Status"
              onChange={handleStatusChange}
            >
              <MenuItem value="all">Todos</MenuItem>
              <MenuItem value="confirmed">Confirmados</MenuItem>
              <MenuItem value="pending">Pendentes</MenuItem>
            </Select>
          </FormControl>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
           <Button
            variant="outlined"
            startIcon={<SendIcon />}
            onClick={handleSendPendingInvitations}
          >
            Enviar Convites
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleOpenAddDialog}
          >
            Adicionar Convidado
          </Button>
        </Box>
      </Box>

      <TableContainer component={Paper} sx={{ boxShadow: 3, borderRadius: 2 }}>
        <Table>
          <TableHead sx={{ backgroundColor: 'primary.main' }}>
            <TableRow>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Nome</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Telefone</TableCell>
              <TableCell align="center" sx={{ color: 'white', fontWeight: 'bold' }}>Status</TableCell>
              <TableCell align="center" sx={{ color: 'white', fontWeight: 'bold' }}>Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredGuests.map((guest: Guest) => (
              <TableRow
                key={guest.id}
                sx={{
                  '&:nth-of-type(odd)': { backgroundColor: 'action.hover' },
                  '&:hover': { backgroundColor: 'action.selected' },
                  transition: 'background-color 0.2s'
                }}
              >
                <TableCell>{guest.name}</TableCell>
                <TableCell>{guest.phone}</TableCell>
                <TableCell align="center">
                  <Tooltip title={guest.confirmed ? "Confirmado" : "Pendente"}>
                    {guest.confirmed ? (
                      <CheckCircleIcon color="success" />
                    ) : (
                      <PendingIcon color="warning" />
                    )}
                  </Tooltip>
                </TableCell>
                <TableCell align="center">
                  <GuestActionsMenu
                    guest={guest}
                    onEdit={handleOpenEditDialog}
                    onDelete={handleOpenDeleteDialog}
                    onConfirmToggle={handleUpdateGuest}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={statistics?.total_guests || 0}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </TableContainer>
      <AddGuestDialog
        open={isAddGuestDialogOpen}
        onClose={handleCloseAddDialog}
        onAddGuest={handleAddGuest}
      />
      {selectedGuest && (
        <EditGuestDialog
          open={isEditGuestDialogOpen}
          onClose={handleCloseEditDialog}
          guest={selectedGuest}
          onEditGuest={handleUpdateGuest}
        />
      )}
      {selectedGuest && (
        <ConfirmDeleteDialog
          open={isDeleteConfirmOpen}
          onClose={handleCloseDeleteDialog}
          onConfirm={() => handleDeleteGuest(selectedGuest.id)}
          title="Confirmar Exclusão"
          description={`Tem certeza que deseja deletar o convidado "${selectedGuest.name}"? Esta ação não pode ser desfeita.`}
        />
      )}
    </Box>
  );
};

export default Guests;