// components/StarsComponent.tsx
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { fetchData, deleteData } from '../api';
import { Star } from '../types';
import UpdateStarForm from './UpdateStarForm';
import './StarsComponent.css';

const StarsComponent: React.FC = () => {
    const queryClient = useQueryClient();
    const [selectedStar, setSelectedStar] = useState<Star | null>(null); // For the star to be updated
    const [isCreating, setIsCreating] = useState(false); // To track if the form is in create mode

    const { data: stars, isLoading } = useQuery<Star[]>(
        'stars',
        () => fetchData<Star[]>('/star', { limit: 10, offset: 0 })
    );

    const deleteStar = useMutation((id: number) => deleteData('/star', { id }), {
        onSuccess: () => queryClient.invalidateQueries('stars'),
    });

    if (isLoading) return <p>Loading stars...</p>;

    return (
        <div className="stars-container">
            <h2>Stars</h2>
            <button onClick={() => { setIsCreating(true); setSelectedStar(null); }}>Create Star</button>
            <ul>
                {stars?.map((star) => (
                    <li key={star.id}>
                        {star.id}: {star.name} - {star.distance_ly} ly
                        <button onClick={() => { setSelectedStar(star); setIsCreating(false); }}>Update</button>
                        <button onClick={() => deleteStar.mutate(star.id)}>Delete</button>
                    </li>
                ))}
            </ul>

            {/* Render UpdateStarForm for creating or updating */}
            {(isCreating || selectedStar) && (
                <UpdateStarForm
                    initialData={selectedStar || undefined}
                    onClose={() => { setSelectedStar(null); setIsCreating(false); }}
                />
            )}
        </div>
    );
};

export default StarsComponent;
