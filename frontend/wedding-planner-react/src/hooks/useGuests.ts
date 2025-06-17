import { useState, useEffect, useMemo } from 'react';
import { SelectChangeEvent } from '@mui/material';
import { guestApi, GuestUpdatePayload, Statistics } from '../lib/api/guest.ts';
import { Guest } from '../types/guest.ts';

export const useGuests = () => {
  const [guests, setGuests] = useState<Guest[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination and Filters
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  // Dialogs and Menus State
  const [isAddGuestDialogOpen, setAddGuestDialogOpen] = useState(false);
  const [isEditGuestDialogOpen, setEditGuestDialogOpen] = useState(false);
  const [isDeleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [selectedGuest, setSelectedGuest] = useState<Guest | null>(null);

  const fetchGuests = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await guestApi.getGuests({
        skip: page * rowsPerPage,
        limit: rowsPerPage
      });
      setGuests(response);
      const statisticsResponse = await guestApi.getStatistics();
      setStatistics(statisticsResponse);
      console.log("statistics", statisticsResponse);
    } catch (err) {
      console.error('Erro ao buscar convidados:', err);
      setError('Falha ao carregar convidados. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGuests();

    // Disabled pagination dependency for now, as backend is not paginating
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, rowsPerPage]);

  const handleAddGuest = async (name: string, phone: string) => {
    await guestApi.addGuest({ name, phone });
    await fetchGuests(); // Refetch guests after adding
  };

  const handleUpdateGuest = async (guestId: number, payload: GuestUpdatePayload) => {
    await guestApi.updateGuest(guestId, payload);
    await fetchGuests();
  };

  const handleDeleteGuest = async (guestId: number) => {
    await guestApi.deleteGuest(guestId);
    await fetchGuests();
  };
  
  const handleSendPendingInvitations = async () => {
    try {
      await guestApi.sendPendingInvitations();
      // Optionally, add a success notification here
    } catch (error) {
      console.error('Erro ao enviar convites:', error);
      setError('Falha ao enviar convites.');
    }
  };

  // Dialog and Menu Handlers
  const handleOpenAddDialog = () => setAddGuestDialogOpen(true);
  const handleCloseAddDialog = () => setAddGuestDialogOpen(false);

  const handleOpenEditDialog = (guest: Guest) => {
    setSelectedGuest(guest);
    setEditGuestDialogOpen(true);
  };
  const handleCloseEditDialog = () => {
    setEditGuestDialogOpen(false);
    setSelectedGuest(null);
  };

  const handleOpenDeleteDialog = (guest: Guest) => {
    setSelectedGuest(guest);
    setDeleteConfirmOpen(true);
  };
  const handleCloseDeleteDialog = () => {
    setDeleteConfirmOpen(false);
    setSelectedGuest(null);
  };


  const filteredGuests = useMemo(() => {
    return guests.filter(guest => {
      const matchesSearch = guest.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           guest.phone.includes(searchTerm);
      const matchesStatus = statusFilter === 'all' ||
                           (statusFilter === 'confirmed' && guest.confirmed) ||
                           (statusFilter === 'pending' && !guest.confirmed);
      return matchesSearch && matchesStatus;
    });
  }, [guests, searchTerm, statusFilter]);

  const confirmedGuestsCount = useMemo(() => guests.filter(g => g.confirmed).length, [guests]);
  const totalGuestsCount = statistics?.total_guests || guests.length; // This should come from the API with pagination
  // Pagination Handlers
  const handleChangePage = async (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const newRowsPerPage = parseInt(event.target.value, 0);
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  // Filter Handlers
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => setSearchTerm(event.target.value);
  const handleStatusChange = (event: SelectChangeEvent) => setStatusFilter(event.target.value as string);

  return {
    // State
    loading,
    error,
    filteredGuests,
    totalGuests: totalGuestsCount,
    confirmedGuests: confirmedGuestsCount,
    statistics,
    
    // Pagination
    page,
    rowsPerPage,
    handleChangePage,
    handleChangeRowsPerPage,

    // Filters
    searchTerm,
    statusFilter,
    handleSearchChange,
    handleStatusChange,
    
    // Dialogs and Actions
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
  };
}; 