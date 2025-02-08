import { z } from "zod";

const MAX_IMAGE_SIZE = 500000;
const ACCEPTED_IMAGE_TYPES = ["image/jpg", "image/jepg", "image/png", "image/webp"]


export const recipeSchema = z.object({
    name: z.string().min(2),
    handle: z.string(),
    description: z.string().min(0),
    instructions: z.string().min(1),
    ingredients: z.object({
        name: z.string().min(1),
        amount: z.coerce.number().positive(),
        unit: z.enum(["cup", "teaspoon","tablespoon","pint","quart","gallon","ounce","fluid ounce","pound","milliliter","liter","gram","kilogram"]),
        recipe: z.string(),
        delete: z.boolean().default(false),
    }).array().min(0),
    // tags: z.string().min(0).array(),
    servings: z.coerce.number().min(1),
    cook_time: z.coerce.number().min(0),
    prep_time: z.coerce.number().min(0),
    visibility: z.coerce.number().min(0),
    // image: z.string().min(0)
    // image: z.object({
    //     image: z
    //     .any()
    //     .refine((file) => file?.size < MAX_IMAGE_SIZE, "Max image size is 5 MB")
    //     .refine((file) => ACCEPTED_IMAGE_TYPES.includes(file?.type), "Only .jpg, .jpeg, .png, and .webp formats supported")
    // }).optional()
    
})

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