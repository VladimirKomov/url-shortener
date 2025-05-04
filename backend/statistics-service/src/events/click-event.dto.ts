export interface ClickEvent {
    short_code: string;
    ip_address: string;
    user_agent?: string;
    referer?: string;
    timestamp: string;
}