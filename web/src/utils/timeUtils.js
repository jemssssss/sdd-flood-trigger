export function getLatestTimeDate() {
  const now = new Date();

  // Round down to the nearest hour
  now.setMinutes(0);
  now.setSeconds(0);
  now.setMilliseconds(0);

  // Format the date using Intl.DateTimeFormat
  const formatter = new Intl.DateTimeFormat("en-US", {
    month: "long",   
    day: "numeric",  
    year: "numeric",    
    //hour: "numeric", 
    //minute: "2-digit", 
    //hour12: true
  });

  return formatter.format(now).replace(",", "");
}