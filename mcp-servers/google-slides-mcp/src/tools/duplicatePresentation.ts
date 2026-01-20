import { drive_v3 } from 'googleapis';
import { DuplicatePresentationArgs } from '../schemas.js';
import { handleGoogleApiError } from '../utils/errorHandler.js';

/**
 * Duplicates a Google Slides presentation using Google Drive API.
 * @param drive The authenticated Google Drive API client.
 * @param args The arguments for duplicating the presentation.
 * @returns A promise resolving to the MCP response with new presentation details.
 * @throws McpError if the Google API call fails.
 */
export const duplicatePresentationTool = async (drive: drive_v3.Drive, args: DuplicatePresentationArgs) => {
  try {
    const response = await drive.files.copy({
      fileId: args.presentationId,
      requestBody: {
        name: args.newName,
      },
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              id: response.data.id,
              name: response.data.name,
              url: `https://docs.google.com/presentation/d/${response.data.id}/edit`,
            },
            null,
            2
          ),
        },
      ],
    };
  } catch (error: unknown) {
    throw handleGoogleApiError(error, 'duplicate_presentation');
  }
};
