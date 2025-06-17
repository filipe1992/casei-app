import React from "react";
import { Link } from "react-router-dom";
import {
  Card,
  Typography,
  List,
  ListItem,
  ListItemPrefix,
} from "@material-tailwind/react";
import {
  HomeIcon,
  UserGroupIcon,
  EnvelopeIcon,
  HeartIcon,
  CalendarIcon,
  GiftIcon,
  PhotoIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/solid";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: HomeIcon, path: "/" },
  { id: "guests", label: "Convidados", icon: UserGroupIcon, path: "/guests" },
  { id: "invitations", label: "Convites", icon: EnvelopeIcon, path: "/invitations" },
  { id: "timeline", label: "Nossa História", icon: HeartIcon, path: "/timeline" },
  { id: "schedule", label: "Cronograma", icon: CalendarIcon, path: "/schedule" },
  { id: "gifts", label: "Lista de Presentes", icon: GiftIcon, path: "/gifts" },
  { id: "photos", label: "Álbum de Fotos", icon: PhotoIcon, path: "/photos" },
  { id: "settings", label: "Configurações", icon: Cog6ToothIcon, path: "/settings" },
];

const Sidebar = ({ isOpen }) => {
  return (
    <Card
      className={`fixed top-16 left-0 z-20 h-[calc(100vh-64px)] bg-white shadow-xl shadow-blue-gray-900/5 transition-all duration-300 ease-in-out 
        ${isOpen ? 'w-80 translate-x-0' : '-translate-x-full w-80 md:w-16 md:translate-x-0'} 
        md:hover:w-80 md:hover:shadow-2xl group peer`}
    >
      <div className={`mb-2 flex items-center gap-4 px-4 py-2 overflow-hidden`}>
        <HeartIcon className="h-8 w-8 text-primary flex-shrink-0" />
        <Typography variant="h5" color="blue-gray" className="whitespace-nowrap transition-opacity duration-300 md:opacity-0 md:group-hover:opacity-100">
          CasaFácil
        </Typography>
      </div>
      <List className="px-2">
        {navItems.map(({ id, label, icon: Icon, path }) => (
          <Link key={id} to={path}>
            <ListItem className="hover:bg-primary/10 focus:bg-primary/20 active:bg-primary/30 gap-4 px-2 py-2">
              <ListItemPrefix>
                <Icon className="h-5 w-5 flex-shrink-0" />
              </ListItemPrefix>
              <Typography color="blue-gray" className="font-normal whitespace-nowrap overflow-hidden transition-opacity duration-300 md:opacity-0 md:group-hover:opacity-100">
                {label}
              </Typography>
            </ListItem>
          </Link>
        ))}
      </List>
    </Card>
  );
};

export default Sidebar;
