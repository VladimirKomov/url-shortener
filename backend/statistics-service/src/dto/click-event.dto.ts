export interface RawClickEventDto {
    short_code: string;
    ip_address: string;
    user_agent?: string;
    referer?: string;
    timestamp: string;
}

export interface ClickEventDto {
    shortCode: string;
    ipAddress: string;
    userAgent?: string;
    referer?: string;
    timestamp: Date;
}

export interface ClickEventResponseDto {
    shortCode: string;
    ipAddress: string;
    userAgent?: string;
    referer?: string;
    timestamp: Date;
}