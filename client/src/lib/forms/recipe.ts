import type { sequence } from "@sveltejs/kit/hooks";
import { z } from "zod";

const MAX_IMAGE_SIZE = 500000;
const ACCEPTED_IMAGE_TYPES = ["image/jpg", "image/jepg", "image/png", "image/webp"]


export const recipeSchema = z.object({
    id: z.number().optional(),
    name: z.string().min(2, "Name must be at least 2 characters."),
    handle: z.string().regex(/^[a-zA-Z0-9_-]+$/, "Handle can only contain letters, numbers, underscores, and hyphens."),
    tag_types: z.array(z.string()).optional(),
    description: z.string().optional().default(""),
    instructions: z.string().optional().default(""),
    ingredients: z.array(
        z.object({
            name: z.string().min(1, "Ingredient name is required."),
            id: z.coerce.number().optional(),
            sequence: z.coerce.number().min(0),
            amount: z.coerce.number().positive("Amount must be a positive number."),
            unit: z.coerce.number().positive("Unit must be a positive number."),
            DELETE: z.boolean().default(false),
        })
    ).optional().default([]), // Allows ingredients to be omitted
    servings: z.coerce.number().min(1, "Servings must be at least 1."),
    cook_time: z.coerce.number().min(0, "Cook time cannot be negative."),
    prep_time: z.coerce.number().min(0, "Prep time cannot be negative."),
    visibility: z.number().default(2),

    // image: z
    //     .any()
    //     .optional()
    //     .refine((file) => !file || (file.size < MAX_IMAGE_SIZE && ACCEPTED_IMAGE_TYPES.includes(file.type)), {
    //         message: "Max image size is 5 MB and only .jpg, .jpeg, .png, and .webp formats are supported."
    //     }),
});

export const imageSchema = z.object({
    title: z.string().min(1),
    alt: z.string().min(0),
    image: z.object({
        image: z
        .any()
        .refine((file) => file?.size < MAX_IMAGE_SIZE, "Max image size is 5 MB")
        .refine((file) => ACCEPTED_IMAGE_TYPES.includes(file?.type), "Only .jpg, .jpeg, .png, and .webp formats supported")
    }).optional()
    
})