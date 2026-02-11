'use client';

import { useState } from 'react';

import Switch from '@mui/material/Switch';

export default function ActionSwitch({ defaultVal, action }) {
  const [checked, setChecked] = useState(defaultVal);

  const handleChange = async (event) => {
    setChecked(event.target.checked);
    const res = await action(event.target.checked);
    if (!res) {
      setChecked((prev) => !prev);
    }
  };

  return (
    <Switch checked={checked} onChange={handleChange} inputProps={{ 'aria-label': 'controlled' }} />
  );
}
