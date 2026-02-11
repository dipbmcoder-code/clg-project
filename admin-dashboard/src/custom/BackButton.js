import React from 'react';

import { Button } from '@mui/material';

import { useRouter, usePathname } from 'src/routes/hooks';

import { BackIcon } from 'src/utils/icons';

const BackButton = ({ pos = -1 }) => {
  const router = useRouter();
  const pathname = usePathname();

  const getPreviousPathname = (pathname, pos) => {
    let index = pathname.length;
    for (let i = 0; i < Math.abs(pos); i++) {
      index = pathname.lastIndexOf('/', index - 1);
      if (index === -1) break;
    }
    return index !== -1 ? pathname.slice(0, index) : pathname;
  };

  const handleBack = (e) => {
    e.preventDefault();
    e.stopPropagation();

    const previousPathname = getPreviousPathname(pathname, pos);
    if (window.history.length > 2) {
      router.back();
    } else {
      router.push(previousPathname);
    }
    router.refresh();
  };

  return (
    <Button
      variant="outlined"
      startIcon={<BackIcon />}
      sx={{
        alignItems: 'center',
      }}
      onClick={handleBack}
    >
      Back
    </Button>
  );
};

export default BackButton;
