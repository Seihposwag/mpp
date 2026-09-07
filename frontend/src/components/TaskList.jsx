import { useEffect, useState } from 'react';
import {
    Container, Typography, Paper, List, ListItem, ListItemText,
    Chip, Box, CircularProgress, Alert,
} from '@mui/material';
import api from '../services/api';

const TaskList = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        api.get('/tasks/')
            .then((response) => setTasks(response.data))
            .catch(() => setError('Не удалось загрузить задачи'))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Container maxWidth="md">
            <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Мои задачи
                </Typography>

                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                {tasks.length === 0 ? (
                    <Typography color="text.secondary">Задач пока нет</Typography>
                ) : (
                    <List>
                        {tasks.map((task) => (
                            <ListItem key={task.id} divider>
                                <ListItemText
                                    primary={task.title}
                                    secondary={task.description || 'Без описания'}
                                />
                                <Chip label={task.status} size="small" sx={{ mr: 1 }} />
                                <Chip label={task.priority} size="small" variant="outlined" />
                            </ListItem>
                        ))}
                    </List>
                )}
            </Paper>
        </Container>
    );
};

export default TaskList;