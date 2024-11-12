// components/UpdatePlanetForm.tsx
import React, { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { createData, updateData } from '../api';
import { Planet } from '../types';

interface UpdatePlanetFormProps {
    initialData?: Planet;
    onClose: () => void;
}

const UpdatePlanetForm: React.FC<UpdatePlanetFormProps> = ({ initialData, onClose }) => {
    const queryClient = useQueryClient();

    // Local state for form inputs, using `initialData` if provided (update mode) or default values (create mode)
    const [name, setName] = useState<string>(initialData?.name || '');
    const [diameterKm, setDiameterKm] = useState<number>(initialData?.diameter_km || 0);
    const [starId, setStarId] = useState<number>(initialData?.star_id || 0);

    // Mutation for creating or updating a planet
    const planetMutation = useMutation(
        (planet: Partial<Planet> & { id?: number }) =>
            initialData
                ? updateData<Planet>('/planet', planet) // Update if initialData exists
                : createData<Planet>('/planet', planet), // Create if initialData is undefined
        {
            onSuccess: () => {
                queryClient.invalidateQueries('planets');
                onClose(); // Close the form after successful creation or update
            },
        }
    );

    // Form submission handler
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (initialData) {
            planetMutation.mutate({ id: initialData.id, name, diameter_km: diameterKm, star_id: starId });
        } else {
            planetMutation.mutate({ name, diameter_km: diameterKm, star_id: starId });
        }
    };

    return (
        <form onSubmit={handleSubmit} className="update-planet-form">
            <h3>{initialData ? 'Update Planet' : 'Create Planet'}</h3>

            <label>
                Name:
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </label>

            <label>
                Diameter (km):
                <input
                    type="number"
                    value={diameterKm}
                    onChange={(e) => setDiameterKm(parseFloat(e.target.value))}
                />
            </label>

            <label>
                Star ID:
                <input
                    type="number"
                    value={starId}
                    onChange={(e) => setStarId(parseInt(e.target.value, 10))}
                />
            </label>

            <button type="submit">{initialData ? 'Save Changes' : 'Create Planet'}</button>
            <button type="button" onClick={onClose}>Cancel</button>
        </form>
    );
};

export default UpdatePlanetForm;
