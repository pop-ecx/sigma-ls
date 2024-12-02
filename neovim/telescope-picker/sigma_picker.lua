local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")
local conf = require("telescope.config").values

local M = {}

-- Utility function to create a floating window
local function create_floating_window(content)
    -- Window dimensions
    local width = math.floor(vim.o.columns * 0.8)
    local height = math.floor(vim.o.lines * 0.8)
    local row = math.floor((vim.o.lines - height) / 2)
    local col = math.floor((vim.o.columns - width) / 2)

    -- Buffer for the floating window
    local buf = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_option(buf, "modifiable", true)

    -- Configure the floating window
    local win = vim.api.nvim_open_win(buf, true, {
        relative = "editor",
        width = width,
        height = height,
        row = row,
        col = col,
        style = "minimal",
        border = "rounded",
    })

    -- Set the content of the buffer
    vim.api.nvim_buf_set_lines(buf, 0, -1, false, content)

    vim.api.nvim_buf_set_keymap(buf, "n", "q", "<cmd>close<CR>", { noremap = true, silent = true })

    return win
end

M.sigma_picker = function(opts)
    opts = opts or {}

    -- supported backends for Sigma Rules
    local sigma_rules = {
        elasticsearch = { "config1.yml", "config2.yml" },
        kibana = { "ecs-auditbeat-modules-enabled", "ecs-auditd","ecs-cloudtrail","ecs-dns","ecs-filebeat","ecs-okta","ecs-proxy","ecs-suricata","ecs-zeek-corelight","ecs-zeek-elastic-beats-implementation","elk-defaultindex","elk-defaultindex-filebeat","elk-defaultindex-logstash","elk-linux","elk-windows","elk-winlogbeat","elk-winlogbeat-sp","filebeat-defaultindex","helk","logstash-defaultindex","logstash-linux","logstash-windows","logstash-zeek-default-json","powershell","sysmon","windows-audit","windows-services","winlogbeat","winlogbeat-modules-enabled", "winlogbeat-old" },
        splunk = { "elk-defaultindex", "elk-defaultindex-filebeat", "elk-defaultindex-logstash", "elk-linux","elk-windows", "elk-winlogbeat", "elk-winlogbeat-sp", "powershell", "splunk-windows", "splunk-windows-index", "splunk-zeek", "sysmon", "windows-audit", "windows-services" },
        crowdstrike = { "crowdstrike","elk-defaultindex", "elk-defaultindex-filebeat", "elk-defaultindex-logstash", "elk-linux", "elk-windows", "elk-winlogbeat", "elk-winlogbeat-sp", "powershell", "sysmon", "windows-audit", "windows-services" },
    }

    -- Picker for configurations
    local function pick_config(selected_backend)
        local configs = sigma_rules[selected_backend]

        pickers.new(opts, {
            prompt_title = "Choose Configuration for " .. selected_backend,
            finder = finders.new_table({
                results = configs,
            }),
            sorter = conf.generic_sorter(opts),
            attach_mappings = function(prompt_bufnr, map)
                actions.select_default:replace(function()
                    local selection = action_state.get_selected_entry()
                    actions.close(prompt_bufnr)

                    local selected_config = selection.value

                    -- Get the currently opened file in the active buffer
                    local current_file = vim.api.nvim_buf_get_name(0)
                    if current_file == "" then
                        print("No file opened in the current buffer!")
                        return
                    end

                    local command =
                        "sigmac -t " ..
                        selected_backend .. " -c " .. selected_config .. " " .. current_file

                    -- Execute the backend converter
                    vim.fn.jobstart(command, {
                        stdout_buffered = true,
                        on_stdout = function(_, data)
                            if data and #data > 0 then
                                -- Filter out empty lines
                                local filtered_data = vim.tbl_filter(function(line)
                                    return line ~= nil and line ~= ""
                                end, data)
                                create_floating_window(filtered_data)
                            end
                        end,
                        on_stderr = function(_, data)
                            if data and #data > 0 then
                                print("Error:", table.concat(data, "\n"))
                            end
                        end,
                        on_exit = function(_, code)
                            if code == 0 then
                                print("Backend converter completed successfully!")
                            else
                                print("Backend converter exited with code:", code)
                            end
                        end,
                    })
                end)
                return true
            end,
        }):find()
    end

   -- Picker for backends
    pickers.new(opts, {
        prompt_title = "Sigma Rules Backend Picker",
        finder = finders.new_table({
            results = vim.tbl_keys(sigma_rules),
        }),
        sorter = conf.generic_sorter(opts),
        attach_mappings = function(prompt_bufnr, map)
            actions.select_default:replace(function()
                local selection = action_state.get_selected_entry()
                actions.close(prompt_bufnr)

                local selected_backend = selection.value
                print("Selected Backend:", selected_backend)

                -- Proceed to configuration picker
                pick_config(selected_backend)
            end)
            return true
        end,
    }):find()
end

return M
