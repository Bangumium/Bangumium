
type Subject = {
    id: number;
    name: string;
    name_cn: string;
    platform: string;
    rating: {
        score: number;
        rank: number;
    }
    summary: string;
    image: string;
    date: string
}

export type { Subject };