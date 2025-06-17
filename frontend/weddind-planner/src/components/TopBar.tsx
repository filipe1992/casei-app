import React from "react";
import {
  Navbar,
  Typography,
  IconButton,
} from "@material-tailwind/react";
import {
  Bars3Icon,
  BellIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/outline";

const TopBar = ({ title, onMenuToggle, user }) => {
  return (
    <Navbar className="fixed top-0 left-0 right-0 z-30 h-16 max-w-full rounded-none px-4 shadow-md bg-white">
      <div className="flex items-center justify-between text-blue-gray-900">
        <div className="flex items-center gap-4">
          <IconButton
            variant="text"
            size="lg"
            onClick={onMenuToggle}
            className="md:hidden"
          >
            <Bars3Icon className="h-6 w-6" />
          </IconButton>
          <Typography variant="h6" className="font-bold">
            {title}
          </Typography>
        </div>

        <div className="flex items-center gap-4">
          <IconButton variant="text" className="rounded-full">
            <BellIcon className="h-5 w-5" />
          </IconButton>

          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
              <UserCircleIcon className="h-6 w-6 text-gray-600" />
            </div>
            <Typography variant="small" className="font-normal">
              {user?.name || "Ana & João"}
            </Typography>
          </div>

          <IconButton variant="text" className="rounded-full">
            <ArrowRightOnRectangleIcon className="h-5 w-5" />
          </IconButton>
        </div>
      </div>
    </Navbar>
  );
};

export default TopBar;
