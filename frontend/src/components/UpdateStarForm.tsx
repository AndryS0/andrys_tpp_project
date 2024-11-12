// components/UpdateStarForm.tsx
import React, { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { createData, updateData } from '../api';
import { Star } from '../types';

interface UpdateStarFormProps {
    initialData?: Star;
    onClose: () => void;
}

const UpdateStarForm: React.FC<UpdateStarFormProps> = ({ initialData, onClose }) => {
    const queryClient = useQueryClient();

    // Local state for form inputs, using `initialData` if provided (update mode) or default values (create mode)
    const [name, setName] = useState<string>(initialData?.name || '');
    const [distanceLy, setDistanceLy] = useState<number>(initialData?.distance_ly || 0);
    const [massSm, setMassSm] = useState<number>(initialData?.mass_sm || 0);

    // Mutation for creating or updating a star
    const starMutation = useMutation(
        (star: Partial<Star> & { id?: number }) =>
            initialData
                ? updateData<Star>('/star', star) // Update if initialData exists
                : createData<Star>('/star', star), // Create if initialData is undefined
        {
            onSuccess: () => {
                queryClient.invalidateQueries('stars');
                onClose(); // Close the form after successful creation or update
            },
        }
    );

    // Form submission handler
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (initialData) {
            starMutation.mutate({ id: initialData.id, name, distance_ly: distanceLy, mass_sm: massSm });
        } else {
            starMutation.mutate({ name, distance_ly: distanceLy, mass_sm: massSm });
        }
    };

    return (
        <form onSubmit={handleSubmit} className="update-star-form">
            <h3>{initialData ? 'Update Star' : 'Create Star'}</h3>

            <label>
                Name:
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </label>

            <label>
                Distance (ly):
                <input
                    type="number"
                    value={distanceLy}
                    onChange={(e) => setDistanceLy(parseFloat(e.target.value))}
                />
            </label>

            <label>
                Mass (solar masses):
                <input
                    type="number"
                    value={massSm}
                    onChange={(e) => setMassSm(parseFloat(e.target.value))}
                />
            </label>

            <button type="submit">{initialData ? 'Save Changes' : 'Create Star'}</button>
            <button type="button" onClick={onClose}>Cancel</button>
        </form>
    );
};

export default UpdateStarForm;
