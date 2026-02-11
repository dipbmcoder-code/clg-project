import AddIcon from '@mui/icons-material/Add';
import SyncIcon from '@mui/icons-material/Sync';
import ErrorIcon from '@mui/icons-material/Error';
import ModeEditIcon from '@mui/icons-material/ModeEdit';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteForeverRoundedIcon from '@mui/icons-material/DeleteForeverRounded';

export function CustomAddIcon() {
  return (
    <AddIcon
      sx={{
        stroke: 'currentColor',
        strokeWidth: 1.5,
      }}
    />
  );
}
export {
  SyncIcon,
  ModeEditIcon as EditIcon,
  CustomAddIcon as AddIcon,
  ArrowBackIcon as BackIcon,
  CheckCircleIcon as CheckIcon,
  ErrorIcon as ExclamationIcon,
  ContentCopyIcon as CopyClipboard,
  DeleteForeverRoundedIcon as DeleteIcon,
};
