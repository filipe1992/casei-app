import React from 'react';
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Button,
  Progress,
} from '@material-tailwind/react';
import {
  UserGroupIcon,
  GiftIcon,
  CalendarIcon,
  PhotoIcon,
  ClockIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/solid';

const StatCard = ({ title, value, icon: Icon, color }) => (
  <Card className="shadow-lg shadow-gray-500/10">
    <CardBody className="p-4">
      <div className="flex items-center gap-4">
        <div className={`rounded-full p-3 ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div>
          <Typography variant="small" color="blue-gray" className="font-normal">
            {title}
          </Typography>
          <Typography variant="h4" color="blue-gray">
            {value}
          </Typography>
        </div>
      </div>
    </CardBody>
  </Card>
);

const TaskCard = ({ title, progress, dueDate }) => (
  <Card>
    <CardBody className="p-4">
      <div className="mb-3 flex items-center justify-between">
        <Typography variant="h6" color="blue-gray">
          {title}
        </Typography>
        <Typography variant="small" color="gray">
          {dueDate}
        </Typography>
      </div>
      <Progress value={progress} color="pink" />
      <div className="mt-2 flex items-center justify-between">
        <Typography variant="small" color="gray">
          {progress}% Completo
        </Typography>
        <CheckCircleIcon className={`h-5 w-5 ${progress === 100 ? 'text-green-500' : 'text-gray-300'}`} />
      </div>
    </CardBody>
  </Card>
);

const WeddingDashboard = () => {
  return (
    <div className="p-4">
      <div className="mb-8">
        <Typography variant="h4" color="blue-gray" className="mb-2">
          Bem-vindos, Ana & João!
        </Typography>
        <Typography variant="paragraph" color="gray" className="font-normal">
          Faltam 120 dias para o grande dia!
        </Typography>
      </div>

      <div className="mb-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <StatCard
          title="Convidados Confirmados"
          value="150/200"
          icon={UserGroupIcon}
          color="bg-pink-500"
        />
        <StatCard
          title="Presentes Escolhidos"
          value="45"
          icon={GiftIcon}
          color="bg-purple-500"
        />
        <StatCard
          title="Dias Restantes"
          value="120"
          icon={CalendarIcon}
          color="bg-blue-500"
        />
      </div>

      <Typography variant="h5" color="blue-gray" className="mb-4">
        Próximas Tarefas
      </Typography>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <TaskCard
          title="Escolher o Buffet"
          progress={75}
          dueDate="15 dias restantes"
        />
        <TaskCard
          title="Enviar Convites"
          progress={30}
          dueDate="30 dias restantes"
        />
        <TaskCard
          title="Prova do Vestido"
          progress={100}
          dueDate="Concluído"
        />
      </div>
    </div>
  );
};

const styles = {
    appContainer: {
        minHeight: '100vh',
        backgroundColor: '#f9fafb',
        display: 'flex',
    },
    sidebar: {
        width: '250px',
        backgroundColor: 'white',
        borderRight: '1px solid #e5e7eb',
        boxShadow: '2px 0 4px rgba(0,0,0,0.1)',
        position: 'fixed',
        height: '100vh',
        left: 0,
        top: 0,
        zIndex: 1000,
    },
    sidebarHidden: {
        transform: 'translateX(-100%)',
        transition: 'transform 0.3s ease',
    },
    sidebarVisible: {
        transform: 'translateX(0)',
        transition: 'transform 0.3s ease',
    },
    sidebarHeader: {
        padding: '20px',
        borderBottom: '1px solid #e5e7eb',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
    },
    logo: {
        fontSize: '20px',
        fontWeight: 'bold',
        color: '#111827',
    },
    sidebarNav: {
        padding: '20px 0',
    },
    navItem: {
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '12px 20px',
        color: '#6b7280',
        cursor: 'pointer',
        transition: 'all 0.2s',
        textDecoration: 'none',
        fontSize: '14px',
        fontWeight: '500',
    },
    navItemActive: {
        backgroundColor: '#fce7f3',
        color: '#be185d',
        borderRight: '3px solid #be185d',
    },
    navItemHover: {
        backgroundColor: '#f3f4f6',
        color: '#374151',
    },
    mainContent: {
        marginLeft: '250px',
        flex: 1,
        minHeight: '100vh',
    },
    mainContentExpanded: {
        marginLeft: 0,
    },
    topBar: {
        backgroundColor: 'white',
        borderBottom: '1px solid #e5e7eb',
        padding: '16px 24px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        position: 'sticky',
        top: 0,
        zIndex: 100,
    },
    topBarTitle: {
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#111827',
    },
    topBarActions: {
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
    },
    mobileMenuButton: {
        display: 'none',
        padding: '8px',
        backgroundColor: 'transparent',
        border: 'none',
        cursor: 'pointer',
    },
    pageContent: {
        marginTop: '64px',
        padding: '24px',
    },
    card: {
        backgroundColor: 'white',
        borderRadius: '8px',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        padding: '24px',
        marginBottom: '24px',
    },
    pageTitle: {
        fontSize: '28px',
        fontWeight: 'bold',
        color: '#111827',
        marginBottom: '8px',
    },
    pageSubtitle: {
        fontSize: '16px',
        color: '#6b7280',
        marginBottom: '24px',
    },
    statsGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        marginBottom: '24px',
    },
    statsCard: {
        backgroundColor: 'white',
        borderRadius: '8px',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        padding: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
    },
    statsIcon: {
        padding: '12px',
        borderRadius: '8px',
    },
    statsIconPink: { backgroundColor: '#fdf2f8', color: '#db2777' },
    statsIconBlue: { backgroundColor: '#eff6ff', color: '#2563eb' },
    statsIconGreen: { backgroundColor: '#f0fdf4', color: '#16a34a' },
    statsIconPurple: { backgroundColor: '#faf5ff', color: '#9333ea' },
    statsValue: {
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#111827',
    },
    statsLabel: {
        fontSize: '14px',
        color: '#6b7280',
    },
    emptyState: {
        textAlign: 'center',
        padding: '60px 20px',
        color: '#6b7280',
    },
    emptyIcon: {
        marginBottom: '16px',
    },
    button: {
        padding: '8px 16px',
        backgroundColor: '#db2777',
        color: 'white',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        fontSize: '14px',
        fontWeight: '500',
        transition: 'background-color 0.2s',
    },
    buttonSecondary: {
        backgroundColor: '#f3f4f6',
        color: '#374151',
    },
};





// Páginas/Componentes

// Dashboard Page
const DashboardPage = () => {
    return (
        <div>
            <div style={styles.statsGrid}>
                <div style={styles.statsCard}>
                    <div style={{ ...styles.statsIcon, ...styles.statsIconPink }}>
                        <Users size={24} />
                    </div>
                    <div>
                        <div style={styles.statsValue}>124</div>
                        <div style={styles.statsLabel}>Total de Convidados</div>
                    </div>
                </div>

                <div style={styles.statsCard}>
                    <div style={{ ...styles.statsIcon, ...styles.statsIconBlue }}>
                        <Gift size={24} />
                    </div>
                    <div>
                        <div style={styles.statsValue}>45</div>
                        <div style={styles.statsLabel}>Lista de Presentes</div>
                    </div>
                </div>

                <div style={styles.statsCard}>
                    <div style={{ ...styles.statsIcon, ...styles.statsIconGreen }}>
                        <Camera size={24} />
                    </div>
                    <div>
                        <div style={styles.statsValue}>89</div>
                        <div style={styles.statsLabel}>Fotos Compartilhadas</div>
                    </div>
                </div>

                <div style={styles.statsCard}>
                    <div style={{ ...styles.statsIcon, ...styles.statsIconPurple }}>
                        <Calendar size={24} />
                    </div>
                    <div>
                        <div style={styles.statsValue}>45</div>
                        <div style={styles.statsLabel}>Dias Restantes</div>
                    </div>
                </div>
            </div>

            <div style={styles.card}>
                <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>
                    Resumo do Casamento
                </h3>
                <p style={{ color: '#6b7280', lineHeight: '1.6' }}>
                    Bem-vindos ao painel de controle do seu casamento! Aqui você pode gerenciar todos os aspectos
                    da sua festa, desde a lista de convidados até o álbum de fotos compartilhado.
                </p>
            </div>
        </div>
    );
};

// Guests Page
const GuestsPage = () => {
    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h2 style={styles.pageTitle}>Lista de Convidados</h2>
                    <p style={styles.pageSubtitle}>Gerencie todos os convidados do seu casamento</p>
                </div>
                <button style={styles.button}>
                    <Plus size={16} style={{ marginRight: '8px' }} />
                    Adicionar Convidado
                </button>
            </div>

            <div style={styles.card}>
                <div style={styles.emptyState}>
                    <Users size={48} color="#d1d5db" style={styles.emptyIcon} />
                    <h3 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '8px' }}>
                        Nenhum convidado cadastrado
                    </h3>
                    <p>Comece adicionando os primeiros convidados da sua lista.</p>
                </div>
            </div>
        </div>
    );
};

// Invitations Page
const InvitationsPage = () => {
    return (
        <div>
            <h2 style={styles.pageTitle}>Convites</h2>
            <p style={styles.pageSubtitle}>Crie e personalize convites para seus convidados</p>

            <div style={styles.card}>
                <div style={styles.emptyState}>
                    <Bell size={48} color="#d1d5db" style={styles.emptyIcon} />
                    <h3 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '8px' }}>
                        Sistema de Convites
                    </h3>
                    <p>Crie convites personalizados e automatize o envio.</p>
                </div>
            </div>
        </div>
    );
};

// Timeline Page
const TimelinePage = () => {
    return (
        <div>
            <h2 style={styles.pageTitle}>Nossa História</h2>
            <p style={styles.pageSubtitle}>Conte a história do casal para os convidados</p>

            <div style={styles.card}>
                <div style={styles.emptyState}>
                    <Heart size={48} color="#d1d5db" style={styles.emptyIcon} />
                    <h3 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '8px' }}>
                        Timeline do Relacionamento
                    </h3>
                    <p>Adicione marcos importantes da sua história juntos.</p>
                </div>
            </div>
        </div>
    );
};

// Schedule Page
const SchedulePage = () => {
    return (
        <div>
            <h2 style={styles.pageTitle}>Cronograma</h2>
            <p style={styles.pageSubtitle}>Organize todos os eventos do seu casamento</p>

            <div style={styles.card}>
                <div style={styles.emptyState}>
                    <Calendar size={48} color="#d1d5db" style={styles.emptyIcon} />
                    <h3 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '8px' }}>
                        Cronograma do Evento
                    </h3>
                    <p>Planeje cada momento do seu dia especial.</p>
                </div>
            </div>
        </div>
    );
};

// Gifts Page
const GiftsPage = () => {
    return (
        <div>
            <h2 style={styles.pageTitle}>Lista de Presentes</h2>
            <p style={styles.pageSubtitle}>Gerencie sua lista de presentes personalizada</p>

            <div style={styles.card}>
                <div style={styles.emptyState}>
                    <Gift size={48} color="#d1d5db" style={styles.emptyIcon} />
                    <h3 style={{ fontSize: '18px', fontWeight: '500', marginBottom: '8px' }}>
                        Loja de Presentes
                    </h3>
                    <p>Configure sua lista de presentes integrada.</p>
                </div>
            </div>
        </div>
    );
};



export default WeddingDashboard;